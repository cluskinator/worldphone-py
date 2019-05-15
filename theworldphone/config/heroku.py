# -*- coding: utf-8 -*-
"""
    config.heroku.py
    ~~~~~~~~~~~~~~~~

    configuration for heroku runtime
"""

import os, urlparse

DEBUG = os.environ.get('DEBUG', True)

DB_NAME = os.environ.get('DB_NAME', 'twp')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', None)
SQLALCHEMY_ECHO = os.environ.get('SQLALCHEMY_ECHO', True)

PREFERRED_URL_SCHEME = 'https'

REDIS_URL = urlparse.urlparse(os.environ.get('REDISCLOUD_URL', 'localhost:6379'))
REDIS_CONFIG = {'host': REDIS_URL.hostname, 'port': REDIS_URL.port, 'password': REDIS_URL.password,
    'db': 0}

TWILIO_ACCOUNT_SID = os.environ.get(
    'TWILIO_ACCOUNT_SID', 'AC9be142691df90581ff106f2f4d97cb11')
TWILIO_API_KEY = os.environ.get(
    'TWILIO_API_KEY', 'SKe048a9e7d475919a5c3ea40d2805b790')
TWILIO_API_SECRET = os.environ.get(
    'TWILIO_API_SECRET', 'm136c441jDFFWlOvKH70tOU8JSRIhAcN')
TWILIO_CONFIGURATION_SID = os.environ.get(
    'TWILIO_CONFIGURATION_SID', 'VS9be142691df90581ff106f2f4d97cb11')
TWILIO_AUTH_TOKEN = os.environ.get(
    'TWILIO_AUTH_TOKEN', '6bd68e118b4d640b3d8bce2bea186428')
TWILIO_APP_SID = os.environ.get(
    'TWILIO_APP_SID', 'AP265a0c55e48929ab42d1c929047d78ab')

TWITTER_KEY = os.environ.get('TWITTER_KEY')
TWITTER_SECRET = os.environ.get('TWITTER_SECRET')
