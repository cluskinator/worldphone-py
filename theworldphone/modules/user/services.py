# -*- coding: utf-8 -*-
"""
    theworldphone.user.services
    ~~~~~~~~~~~~~~~~

    user resource API endpoints and controllers
"""

from flask import Blueprint, current_app, jsonify, make_response, request
from flask_restful import Api, Resource
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
import requests

from theworldphone.decorators import auth_required
from theworldphone.extensions import db

from .constants import COUNTRY_CODES
from .models import User, UserSchema, Language, LanguageSchema, RatingSchema


user = Blueprint('user', __name__)

api = Api(user)
# api.representations['Content-Type'] = 'Authorization'

schema = UserSchema(strict=True)
language_schema = LanguageSchema()
languages_schema = LanguageSchema(many=True)
ratings_schema = RatingSchema(many=True)


class GetCurrentUser(Resource):
    method_decorators = [auth_required]

    def get(self):
        _user = requests.post('https://%s/tokeninfo' % current_app.config.get('AUTH0_DOMAIN', None),
            json={'id_token': request.headers.get('Authorization', None).split()[1]},
            headers={'Content-Type': 'application/json'}
        )
        user = _user.json()
        query = User().first(auth0_user_id=user['user_id']) or \
            User().create(**{
                'auth0_user_id': user['user_id'],
                'name': user['nickname'],
                'email': user['email']})
        results = schema.dump(query).data
        return results, 201


class CreateUser(Resource):
    method_decorators = [auth_required]

    def post(self):
        raw_dict = request.get_json(force=True)
        try:
            schema.validate(raw_dict)
            request_dict = raw_dict['data']['attributes']
            user = User().create(**request_dict)
            results = schema.dump(user).data
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


class GetUpdateDeleteUser(Resource):
    method_decorators = [auth_required]

    # Gets a few details for call partners
    def get(self, uid):
        user = User().first(uid=uid)
        try:
            results = {
                'data': {
                    'type': 'user',
                    'attributes': {
                        'id': user.uid,
                        'nickname': user.name,
                        'country': COUNTRY_CODES[user.location],
                        'fluent': user.spoken_languages[0].name
                    }
                }
            }
            print results
            return results, 201

        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 401
            return resp

    def patch(self, uid):
        user = User().first(uid=uid)
        raw_dict = request.get_json(force=True)
        try:
            schema.validate(raw_dict)
            request_dict = raw_dict['data']['attributes']
            relationships = raw_dict['data']['relationships']

            # Languages
            spoken_uids = [lang['id'] for lang in relationships['spoken_languages']['data']]
            learning_uids = [lang['id'] for lang in relationships['learning_languages']['data']]
            user = user.update_languages(spoken_uids, learning_uids)

            # Ratings
            if not user.ratings.all():
                user.init_ratings()  # Creates starting ratings

            if 'ratings' in relationships:
                user.set_ratings(relationships['ratings'])

            query = User().update(user, **request_dict)
            results = schema.dump(query).data
            return results, 201
            # return self.get(id)

        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 401
            return resp

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 401
            return resp

    # http://jsonapi.org/format/#crud-deleting
    # A server MUST return a 204 No Content status code if a deletion request
    # is successful and no content is returned.
    def delete(self, uid):
        user = User().first(uid=uid)
        try:
            User().delete(user)
            response = make_response()
            response.status_code = 204
            return response

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 401
            return resp


class UpdateUserLanguages(Resource):
    method_decorators = [auth_required]

    def patch(self, uid):
        user = User().first(uid=uid)
        raw_dict = request.get_json(force=True)
        try:
            relationships = raw_dict['data']['relationships']
            spoken_uids = []
            learning_uids = []
            if 'spoken_languages' in relationships:
                spoken_uids = [lang['id'] for lang in relationships['spoken_languages']['data']]
            if 'learning_languages' in relationships:
                learning_uids = [lang['id'] for lang in relationships['learning_languages']['data']]
            user.update_languages(spoken_uids, learning_uids)

            return 'success', 201  # this is silly.

        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 401
            return resp

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 401
            return resp


class UserRatings(Resource):
    method_decorators = [auth_required]

    def patch(self, uid):
        user = User().first(uid=uid)
        raw_dict = request.get_json(force=True)
        try:
            schema.validate(raw_dict)
            relationships = raw_dict['data']['relationships']

            if 'ratings' in relationships:
                user.set_ratings(relationships['ratings'])

            results = schema.dump(user).data
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


class GetCountries(Resource):
    method_decorators = [auth_required]

    def get(self):
        return COUNTRY_CODES


class GetLanguages(Resource):
    method_decorators = [auth_required]

    def get(self):
        languages = Language().all()
        results = languages_schema.dump(languages).data
        return results, 201

api.add_resource(GetCurrentUser, '/users/current/')
api.add_resource(CreateUser, '/users/')
api.add_resource(GetUpdateDeleteUser, '/users/<string:uid>')
api.add_resource(UpdateUserLanguages, '/users/<string:uid>/languages')
api.add_resource(UserRatings, '/users/<string:uid>/ratings')
api.add_resource(GetCountries, '/countries/')
api.add_resource(GetLanguages, '/languages/')
