# -*- coding: utf-8 -*-
"""
    theworldphone.decorators
    ~~~~~~~~~~~~~~~~

    decorator functions
"""

import jwt
import base64

from functools import wraps

from flask import abort, current_app, jsonify, request
from flask.ext.login import current_user


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


# Authentication attribute/annotation
def authenticate(error):
    resp = jsonify(error)
    resp.status_code = 401
    return resp


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', None)
        if not auth:
            return authenticate({
                'code': 'authorization_header_missing',
                'description': 'Authorization header is expected'})

        parts = auth.split()

        if parts[0].lower() != 'bearer':
            return {'code': 'invalid_header',
                'description': 'Authorization header must start with Bearer'}
        elif len(parts) == 1:
            return {'code': 'invalid_header',
                'description': 'Token not found'}
        elif len(parts) > 2:
            return {'code': 'invalid_header',
                'description': 'Authorization header must be Bearer + \s + token'}

        token = parts[1]
        try:
            payload = jwt.decode(
                token,
                base64.b64decode(
                    current_app.config['AUTH0_CLIENT_SECRET'].replace("_", "/").replace("-", "+")),
                audience=current_app.config['AUTH0_CLIENT_ID']
            )
        except jwt.ExpiredSignature:
            return authenticate({'code': 'token_expired',
                'description': 'token is expired'})
        except jwt.InvalidAudienceError:
            return authenticate({'code': 'invalid_audience',
                'description': 'incorrect audience, expected: 4hsMGdHDV4AQSYjzXmFQGrHEYy7nw8D0'})
        except jwt.DecodeError:
            return authenticate({'code': 'token_invalid_signature',
                'description': 'token signature is invalid'})

        current_user = user = payload
        return f(*args, **kwargs)

    return decorated
