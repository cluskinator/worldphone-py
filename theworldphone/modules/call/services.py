# -*- coding: utf-8 -*-
"""
    theworldphone.call.services
    ~~~~~~~~~~~~~~~~

    call resource API endpoints and controllers
"""

from flask import Blueprint, current_app, jsonify, make_response, request
from flask_restful import Api, Resource
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from logging import getLogger

import base64, re, requests
from datetime import datetime
from urllib import unquote

from twilio.rest import TwilioRestClient
from twilio.util import TwilioCapability
from twilio.access_token import AccessToken, ConversationsGrant

from theworldphone.decorators import auth_required
from theworldphone.extensions import db
from theworldphone.modules.redis import RedisQueue
from theworldphone.modules.user import User
from theworldphone.modules.user.models import Language

from .constants import DEFAULT_TOPICS, DEFAULT_TRENDS, WOEID
from .models import CallLog, CallLogSchema

log = getLogger('theworldphone')

call_log = Blueprint('call_log', __name__)

api = Api(call_log)
# api.representations['Content-Type'] = 'Authorization'

schema = CallLogSchema(strict=True)


# Call Logs


class GetCallLogs(Resource):
    method_decorators = [auth_required]

    def get(self, user_uid):
        call_logs = CallLog().with_user(user_uid)
        results = schema.dump(call_logs, many=True).data
        return results, 201


class CreateCallLog(Resource):
    method_decorators = [auth_required]

    def post(self):
        raw_dict = request.get_json(force=True)
        try:
            schema.validate(raw_dict)
            request_dict = raw_dict['data']['attributes']
            request_dict['account_sid'] = current_app.config['TWILIO_ACCOUNT_SID']
            request_dict['app_sid'] = current_app.config['TWILIO_APP_SID']
            call_log = CallLog().create(**request_dict)
            results = schema.dump(call_log).data
            return results, 201

        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 403
            return resp

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 403
            return resp


class UpdateDeleteCallLog(Resource):  # For standard update/delete
    method_decorators = [auth_required]

    def patch(self, uid):
        call_log = CallLog().first(uid=uid)
        raw_dict = request.get_json(force=True)
        try:
            schema.validate(raw_dict)
            request_dict = raw_dict['data']['attributes']

            query = CallLog().update(call_log, **request_dict)
            results = schema.dump(query).data
            return results, 201

        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 401
            return resp

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 401
            return resp

    def delete(self, uid):
        try:
            call_log = CallLog().first(uid=uid)
            CallLog().delete(call_log)
            return '', 204

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 401
            return resp


class UpdateCallSurvey(Resource):  # For post-call updates (w/ call_sid)
    method_decorators = [auth_required]

    def patch(self, sid):
        call_log = CallLog().first(call_sid=sid)
        raw_dict = request.get_json(force=True)
        try:
            schema.validate(raw_dict)
            request_dict = raw_dict['data']['attributes']

            # Set call quality
            user_uid = request_dict.get('current_user')
            quality_rating = request_dict.get('quality', 0)
            if user_uid == call_log.caller_uid:
                call_log.caller_quality = quality_rating
            else:
                call_log.callee_quality = quality_rating

            # Set abuse flag/comment
            flag = request_dict.get('flag')
            comment = request_dict.get('comment', '')
            if flag or comment:
                call_log.add_comment(user_uid, comment, flag)

            # Update call log
            query = CallLog().update(call_log)
            results = schema.dump(query).data
            return results, 201

        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 401
            return resp

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 401
            return resp


# Calls


class GetCallToken(Resource):
    method_decorators = [auth_required]

    def get(self, user_uid):
        token = twilio_token()     # Create a token for Twilio auth and connection
        token.identity = user_uid  # Set the identity of this token
        return jsonify(identity=token.identity, token=token.to_jwt())  # Return token info as JSON


class GetCallTopics(Resource):
    method_decorators = [auth_required]

    def get(self):
        # Twitter trends
        trends = []

        url = 'https://api.twitter.com/1.1/trends/place.json?id=' + str(WOEID)
        headers = {'Authorization': 'Bearer ' + twitter_token()}

        response = requests.get(url, headers=headers)
        response_json = response.json()
        if response_json and isinstance(response_json, list):
            raw_trends = response_json[0].get('trends')
            for trend in raw_trends:
                trend_name = re.sub(r"\"", "", re.sub(r"\+", " ", unquote(trend.get('query'))))
                if '#' in trend_name:
                    trends.append(trend_name)

        if not trends:
            trends = DEFAULT_TRENDS

        resp = {
            'data': {
                'attributes': {
                    'trends': trends,
                    'topics': DEFAULT_TOPICS
                }
            }
        }

        return resp, 200


class QueueCalls(Resource):
    method_decorators = [auth_required]

    def post(self):  # Make call
        raw_dict = request.get_json(force=True)
        request_dict = raw_dict['data']['attributes']

        token = twilio_token()
        current_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        caller = User().first(uid=request_dict['caller_identity'])

        # Queue format: 'user_uid:user_ip'

        call_type = request_dict.get('call_type')
        call_languages = request_dict.get('call_languages')
        queue_name = CallLog.queue_name(call_type, call_languages)
        queue = RedisQueue(name=queue_name, **current_app.config['REDIS_CONFIG'])

        if call_type == 'random':
            partner_queue = queue
        else:
            partner_queue_name = CallLog.queue_name(call_type, call_languages.reverse())
            partner_queue = RedisQueue(name=partner_queue_name,
                **current_app.config['REDIS_CONFIG'])

        partner_uid = caller.uid
        while partner_uid == caller.uid:  # keep going only if partner is self
            partner = partner_queue.pop()
            partner_uid = partner.split(':')[0] if partner else None

        if not partner:
            user_info = ':'.join((str(request_dict['caller_identity']),
                request.environ.get('HTTP_X_REAL_IP', request.remote_addr)))
            queue.push(user_info)

            attributes = {
                'waiting': True,
                'queue_name': queue_name
            }
        else:
            partner_data = partner.split(':')
            partner_uid = partner_data[0]
            partner = User().first(uid=partner_uid)

            current_ip = str(current_ip)
            partner_ip = str(partner_data[1])
            # Tracking format: 'user1:user2:ip1:ip2'
            track_item = ':'.join((caller.uid, partner_uid, current_ip, partner_ip))
            tracking_queue = RedisQueue('current_calls', **current_app.config['REDIS_CONFIG'])
            tracking_queue.push(track_item)

            # Create CallLog
            if call_languages:
                language1 = call_languages[0]
                language2 = language1  # language1 == language2 if single language call
                if len(request_dict['call_languages']) > 1:
                    language2 = request_dict['call_languages'][1]

            call_log_details = {
                'account_sid': current_app.config['TWILIO_ACCOUNT_SID'],
                'app_sid': current_app.config['TWILIO_APP_SID'],
                'caller_uid': caller.uid,
                'callee_uid': partner.uid,
                'caller_ip': current_ip,
                'callee_ip': partner_ip,
                'caller_username': caller.name,
                'callee_username': partner.name,
                'language1_uid': language1,
                'language2_uid': language2,
                'start_time': datetime.utcnow()
            }
            call_log = CallLog(**call_log_details)
            call_log = CallLog().save(call_log)

            attributes = {
                'call_log_uid': call_log.uid,
                'partner': partner.uid,
                'waiting': False,
                'queue_name': queue_name
            }

        resp = {
            'data': {
                'type': 'call',
                'attributes': attributes
            }
        }

        log_call_attempt(caller, queue_name, partner)
        return resp, 200

    def patch(self):  # End call
        raw_dict = request.get_json(force=True)
        request_dict = raw_dict['data']['attributes']

        if request_dict.get('call_log_uid'):
            # Update call log with end time
            call_log = CallLog().first(uid=request_dict['call_log_uid'])
            call_log.end_time = datetime.utcnow()
            call_log = CallLog().save(call_log)

            # Remove from tracking queue
            item1 = ':'.join((call_log.caller_uid, call_log.callee_uid,
                              call_log.caller_ip, call_log.callee_ip))
            item2 = ':'.join((call_log.callee_uid, call_log.caller_uid,
                              call_log.callee_ip, call_log.caller_ip))

            tracking_queue = RedisQueue('current_calls', **current_app.config['REDIS_CONFIG'])
            tracking_queue.rem(item1)
            tracking_queue.rem(item2)

        else:
            # Remove from waiting queue
            queue_name = CallLog.queue_name(request_dict.get('call_type'),
                request_dict.get('call_languages'))
            item = ':'.join((request_dict.get('caller_identity'),
                request.environ.get('HTTP_X_REAL_IP', request.remote_addr)))
            queue = RedisQueue(name=queue_name, **current_app.config['REDIS_CONFIG'])
            queue.rem(item)
        return '', 204


def twilio_token():
    # get credentials for environment variables
    account_sid = current_app.config['TWILIO_ACCOUNT_SID']
    api_key = current_app.config['TWILIO_API_KEY']
    api_secret = current_app.config['TWILIO_API_SECRET']

    # Create an Access Token
    token = AccessToken(account_sid, api_key, api_secret)

    # Grant access to Conversations
    grant = ConversationsGrant()
    grant.configuration_profile_sid = current_app.config['TWILIO_CONFIGURATION_SID']
    token.add_grant(grant)

    return token


def twitter_token():
    consumer_key = current_app.config['TWITTER_KEY']
    consumer_secret = current_app.config['TWITTER_SECRET']

    bearer_token = '%s:%s' % (consumer_key, consumer_secret)
    encoded_bearer_token = base64.b64encode(bearer_token.encode('ascii'))

    url = 'https://api.twitter.com/oauth2/token'
    headers = {
        'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'authorization': 'Basic %s' % encoded_bearer_token.decode('utf-8')
    }
    data = {'grant_type': 'client_credentials'.encode('ascii')}

    response = requests.post(url, headers=headers, data=data)
    access_token = response.json().get('access_token')

    return access_token


def log_call_attempt(caller, queue_name, partner):
    attr = request.get_json(force=True)['data']['attributes']
    call_type = attr.get('call_type', '<missing>')
    call_languages = attr.get('call_languages', [])
    languages = []
    for language_uid in call_languages:
        languages.append(Language().first(uid=language_uid).name)
    languages = ', '.join(languages) if languages else '<missing>'

    if partner:
        matched = 'Matched'
        partner_details = '%s (%s)' % (partner.name, partner.uid)
    else:
        matched = 'Queued'
        partner_details = 'None'

    log.info(
        """
    Caller:     {caller_details}
    Queue:      {queue}
    Call Type:  {call_type}
    Language:   {language}
    Status:     {matched}
    Partner:    {partner_details}
    Time [UTC]: {current_time}
        """.format(
            caller_details='%s (%s)' % (caller.name, caller.uid),
            queue=queue_name,
            language=languages,
            call_type=call_type,
            matched=matched,
            partner_details=partner_details,
            current_time=datetime.utcnow()
        ))


# Call logs
api.add_resource(GetCallLogs, '/call_logs/<string:user_uid>')
api.add_resource(CreateCallLog, '/call_logs/')
api.add_resource(UpdateDeleteCallLog, '/call_logs/<string:uid>')
api.add_resource(UpdateCallSurvey, '/call_survey/<string:sid>')

# Calls
api.add_resource(GetCallToken, '/calls/token/<string:user_uid>')
api.add_resource(GetCallTopics, '/calls/topics/')
api.add_resource(QueueCalls, '/calls/')
