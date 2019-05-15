# -*- coding: utf-8 -*-
"""
    theworldphone.modules.call.views
    ~~~~~~~~~~~~~~~~

    call module views and controllers
"""

from flask import current_app, request, render_template, abort, Blueprint, jsonify
from flask.ext.login import current_user, login_required
from sqlalchemy import or_
from twilio.util import TwilioCapability
from twilio.rest import TwilioRestClient
from twilio.access_token import AccessToken, ConversationsGrant

import base64, json, os, re, time
from urllib import unquote
from uuid import uuid4
from random import randint
from datetime import datetime
import requests
from requests.auth import HTTPBasicAuth

from theworldphone.modules.redis import RedisQueue, RedisHash
from theworldphone.extensions import db
from theworldphone.modules.user import User, LANGUAGES, TOPICS

from .models import CallLog
from .constants import CALL_TYPES

call = Blueprint('call', __name__, url_prefix='/call')


# @call.route('/token/<caller_identity>')
# def token(caller_identity):
#     # Create a token for Twilio auth and connection
#     token = generate_token()
#
#     # Set the identity of this token
#     token.identity = caller_identity
#
#     # Return token info as JSON
#     return jsonify(identity=token.identity, token=token.to_jwt())


# @call.route('/twitter_trends')
# def twitter_trends():
#     access_token = get_twitter_token()
#
#     woeid = 23424977  # United States
#     url = 'https://api.twitter.com/1.1/trends/place.json?id=' + str(woeid)
#     headers = {'Authorization': 'Bearer ' + access_token}
#
#     response = requests.get(url, headers=headers)
#     response_json = response.json()
#     if response_json:
#         raw_trends = response_json[0].get('trends')
#         trends = []
#         for trend in raw_trends:
#             trend_name = re.sub(r"\"", "", re.sub(r"\+", " ", unquote(trend.get('query'))))
#             if '#' in trend_name:
#                 trends.append(trend_name)
#     else:
#         trends = [
#             '#AddGoatRuinAQuote',
#             '#GameOfThrones',
#             '#IDontGenerally',
#             '#Kanye',
#             '#lemons',
#             '#MyJobDescriptionIn5Words',
#             '#TheMuppets',
#             '#ThingsThatIForget'
#         ]
#     return jsonify(trends=trends)


# @call.route('/end_call', methods=['PUT'])
# def end_call():
#     '''This function removes a user from the redis queue.
#
#     POST Variables:
#         - data: A dictionary containing the following values
#         - queue: The current queue the user is in
#         - id: The ID of the current user
#         - room_id: The TogetherJS hub room_id the current user is in
#         - ip: The users IP address
#         - paired_id: id of the partner user if manually paired
#         - room_topic: assigned topic of the room
#
#
#     Returns:
#         If user is successfully removed, returns JSON object containing the call_sid they were in.
#     '''
#     data = json.loads(request.data)
#     if data.get('call_log_uid'):
#         # remove from tracking queue and update call log with end time
#         call_log = CallLog().first(uid=data['call_log_uid'])
#         call_log.end_time = datetime.now()
#         call_log = CallLog().save(call_log)
#
#         item1 = ':'.join((call_log.caller_uid, call_log.callee_uid,
#                           # call_log.caller_location, call_log.callee_location,
#                           call_log.caller_ip, call_log.callee_ip))
#         item2 = ':'.join((call_log.callee_uid, call_log.caller_uid,
#                           # call_log.callee_location, call_log.caller_location,
#                           call_log.callee_ip, call_log.caller_ip))
#
#         tracking_queue = RedisQueue('current_calls', **current_app.config['REDIS_CONFIG'])
#         tracking_queue.rem(item1)
#         tracking_queue.rem(item2)
#
#     elif data.get('call_type') and data.get('call_languages') and data.get('caller_identity'):
#         # remove from waiting queue
#         if data['call_type'] == 'random':
#             queue_name = 'r_' + data['call_languages'][0]
#         elif data['call_type'] == 'exchange':
#             queue_name = 'ex_' + data['call_languages'][0] + '_' + data['call_languages'][1]
#
#         item = ':'.join((data['caller_identity'],
#             request.environ.get('HTTP_X_REAL_IP', request.remote_addr)))
#         queue = RedisQueue(name=queue_name, **current_app.config['REDIS_CONFIG'])
#         queue.rem(item)
#
#     return jsonify({'status': 'success'})


# @call.route('/make_call', methods=['POST'])
# # @login_required
# def make_call():
#     """
#     This function creates the route endpoint for making any type of call.
#     All variables are posted in a JSON that is loaded in the function.
#
#     POST Variables:
#         - caller_identity (str): uid for the current user
#         - call_languages ( ): list containing either one or two language ids
#
#     Returns:
#        json for the appropriate response, whether queued (waiting) or paired (ready to connect).
#     """
#
#     data = json.loads(request.data)
#     token = generate_token()
#     current_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
#
#     caller = User().first(uid=data['caller_identity'])
#
#     # Queue format: 'user_uid:user_ip'
#
#     # RANDOM CALL
#     if data['call_type'] == 'random':
#         language = data['call_languages'][0]
#
#         queue_name = 'r_' + language
#         queue = RedisQueue(name=queue_name, **current_app.config['REDIS_CONFIG'])
#
#         partner_queue = queue
#
#     # EXCHANGE CALL // not really initially supported
#     elif data['call_type'] == 'exchange':
#         spoken_language = data['call_languages'][0]
#         learning_language = data['call_languages'][1]
#
#         queue_name = 'ex_' + spoken_language + '_' + learning_language
#         queue = RedisQueue(name=queue_name, **current_app.config['REDIS_CONFIG'])
#
#         partner_queue_name = 'ex_' + learning_language + '_' + spoken_language
#         partner_queue = RedisQueue(name=partner_queue_name, **current_app.config['REDIS_CONFIG'])
#
#     # TEFL CALL // no longer supported
#     # elif data['call_type'] == 'tefl':
#     #     if caller.is_tefl():
#     #         queue = RedisQueue(name='t_instructor', **current_app.config['REDIS_CONFIG'])
#     #         partner_queue = RedisQueue(name='t_student', **current_app.config['REDIS_CONFIG'])
#     #     else:
#     #         queue = RedisQueue(name='t_student', **current_app.config['REDIS_CONFIG'])
#     #         partner_queue = RedisQueue(name='t_instructor', **current_app.config['REDIS_CONFIG'])
#
#     partner_uid = caller.uid
#     while partner_uid == caller.uid:  # keep going only if partner is self
#         partner = partner_queue.pop()
#         partner_uid = partner.split(':')[0] if partner else None
#
#     if not partner:
#         user_info = ':'.join((str(data['caller_identity']),
#             request.environ.get('HTTP_X_REAL_IP', request.remote_addr)))
#         queue.push(user_info)
#
#         r = {
#             'waiting': True,
#             'queue_name': queue_name
#         }
#         return jsonify(r)
#
#     else:
#         partner_data = partner.split(':')
#         partner_uid = partner_data[0]
#         partner_ip = partner_data[1]
#
#         partner = User().first(uid=partner_uid)
#
#         locations = [str(caller.location), str(partner.location)]
#         ips = [str(current_ip), str(partner_ip)]
#
#         # Tracking format: 'user1:user2:ip1:ip2'  # 'user1:user2:location1:location2:ip1:ip2'
#         track_item = ':'.join((
#             str(caller.uid),
#             str(partner_uid),
#             # locations[0],  # Do we really need
#             # locations[1],  #  these locations?
#             ips[0],
#             ips[1]))
#         tracking_queue = RedisQueue('current_calls', **current_app.config['REDIS_CONFIG'])
#         tracking_queue.push(track_item)
#
#         # Create CallLog
#         if data['call_languages']:
#             language1 = data['call_languages'][0]
#             language2 = language1  # language1 == language2 if single language call
#             if len(data['call_languages']) > 1:
#                 language2 = data['call_languages'][1]
#
#         call_log_details = {
#             'account_sid': current_app.config['TWILIO_ACCOUNT_SID'],
#             'app_sid': current_app.config['TWILIO_APP_SID'],
#             'caller_uid': caller.uid,
#             'callee_uid': partner.uid,
#             'caller_ip': ips[0],
#             'callee_ip': ips[1],
#             'caller_username': caller.name,
#             'callee_username': partner.name,
#             'language1_uid': language1,
#             'language2_uid': language2,
#             'start_time': datetime.now()
#         }
#         call_log = CallLog(**call_log_details)
#         call_log = CallLog().save(call_log)
#
#         # TEMPORARY?
#         r = {
#             'call_log_uid': call_log.uid,
#             'partner': partner.uid,
#             'waiting': False,
#             'queue_name': queue_name
#         }
#         return jsonify(r)


# def generate_token():
#     # get credentials for environment variables
#     account_sid = current_app.config['TWILIO_ACCOUNT_SID']
#     api_key = current_app.config['TWILIO_API_KEY']
#     api_secret = current_app.config['TWILIO_API_SECRET']
#
#     # Create an Access Token
#     token = AccessToken(account_sid, api_key, api_secret)
#
#     # Grant access to Conversations
#     grant = ConversationsGrant()
#     grant.configuration_profile_sid = current_app.config['TWILIO_CONFIGURATION_SID']
#     token.add_grant(grant)
#
#     return token
#
#
# def get_twitter_token():
#     consumer_key = current_app.config['TWITTER_KEY']
#     consumer_secret = current_app.config['TWITTER_SECRET']
#
#     bearer_token = '%s:%s' % (consumer_key, consumer_secret)
#     encoded_bearer_token = base64.b64encode(bearer_token.encode('ascii'))
#
#     url = 'https://api.twitter.com/oauth2/token'
#     headers = {
#         'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
#         'authorization': 'Basic %s' % encoded_bearer_token.decode('utf-8')
#     }
#     data = {'grant_type': 'client_credentials'.encode('ascii')}
#
#     response = requests.post(url, headers=headers, data=data)
#     access_token = response.json().get('access_token')
#
#     return access_token
