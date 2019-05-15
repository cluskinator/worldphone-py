# -*- coding: utf-8 -*-
"""
    theworldphone.modules.api.views
    ~~~~~~~~~~~~~~~~

    api module controllers
"""

from flask import Blueprint
from flask_restful import Api, Resource

from theworldphone.decorators import auth_required


api = Blueprint('api', __name__)
_api = Api(api)
# _api.representations['Content-Type'] = 'Authorization'


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class AuthHelloWorld(Resource):
    method_decorators = [auth_required]

    def get(self):
        return {'hello': 'authenticated world'}

_api.add_resource(HelloWorld, '/')
_api.add_resource(AuthHelloWorld, '/auth/')
