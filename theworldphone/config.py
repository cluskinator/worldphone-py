# -*- coding: utf-8 -*-
"""
    theworldphone.config
    ~~~~~~~~~~~~~~~~

    base configuration classes
"""

import os

from utils import make_dir, INSTANCE_FOLDER_PATH


class BaseConfig(object):

    PROJECT = "theworldphone"
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    ADMINS = ['support+worldphone@cuttlesoft.com']

    # http://flask.pocoo.org/docs/quickstart/#sessions
    SECRET_KEY = 'howling.corvette+cutlass-F15'

    LOG_FOLDER = os.path.join(INSTANCE_FOLDER_PATH, 'logs')
    UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'theworldphone/static/uploads')
    CLIENT_FOLDER = os.path.join(PROJECT_ROOT, 'theworldphone/static/client')
    make_dir(LOG_FOLDER)
    make_dir(UPLOAD_FOLDER)

    # Fild upload, should override in production.
    # Limited the maximum allowed payload to 16 megabytes.
    # http://flask.pocoo.org/docs/patterns/fileuploads/#improving-uploads
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    TRANSLATIONS_FOLDER = os.path.join(PROJECT_ROOT, 'translations')
    TRANSLATIONS_PATH = 'LC_MESSAGES/'
    TRANSALTIONS_FILE = 'messages.po'


class DefaultConfig(BaseConfig):

    DEBUG = True
    TESTING = False

    # the api prefix is the path to api endpoints, leave off the trailing slash
    API_PREFIX = '/api/v1'

    # Flask-Sqlalchemy: http://packages.python.org/Flask-SQLAlchemy/config.html
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + INSTANCE_FOLDER_PATH + '/db.sqlite'

    # Flask-babel: http://pythonhosted.org/Flask-Babel/
    ACCEPT_LANGUAGES = ['en', 'es', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'

    LANGUAGES = {
        'en': u'English',
        'es': u'Español',
        'fr': u'Français'
    }

    # Flask-cache: http://pythonhosted.org/Flask-Cache/
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 60

    # Mailchimp
    MAILCHIMP_API_KEY = 'f0acc728c7bd5aac090c31a3223f1f08-us10'

    # Sendgrid
    SENDGRID_USERNAME = 'phonebot'
    SENDGRID_PASSWORD = 'pulpfiction'

    # Twilio
    TWILIO_ACCOUNT_SID = 'AC9be142691df90581ff106f2f4d97cb11'
    TWILIO_API_KEY = 'SKe048a9e7d475919a5c3ea40d2805b790'
    TWILIO_API_SECRET = 'm136c441jDFFWlOvKH70tOU8JSRIhAcN'
    TWILIO_CONFIGURATION_SID = 'VS9be142691df90581ff106f2f4d97cb11'
    TWILIO_AUTH_TOKEN = '6bd68e118b4d640b3d8bce2bea186428'
    TWILIO_APP_SID = 'AP265a0c55e48929ab42d1c929047d78ab'

    # Twitter
    TWITTER_KEY = 'srzSZ7MvR6oVbmCLCMldOthxA'  # Cuttlesoft dev key
    TWITTER_SECRET = 'MiW8TKnKu8Lft7VL6iHM56zLqRJEOfMMaepsStA0oVUVTMM3QD'  # Cuttlesoft dev secret

    # Auth0
    AUTH0_DOMAIN = 'theworldphone.auth0.com'
    AUTH0_CLIENT_ID = '4hsMGdHDV4AQSYjzXmFQGrHEYy7nw8D0'
    AUTH0_CLIENT_SECRET = 'krHEhvSeuJPqPwGXRdi086Izaotbcjf_mHWcjt2hRYblEpWjL3qBbhvtlY4zKF6k'
    AUTH0_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJ4QmNlRzVLNXZ0N3ppTzBTN1RISTVXQ1pLNFFXMU1nYSIsInNjb3BlcyI6e30sImlhdCI6MTQ1MjcxNTEzNCwianRpIjoiMTFhOGM3Njg0OWYzNjk0ZmM1NmNhN2JiZWIyNWQyZmEifQ.LRIuOSbtncmEYzizOpxeZjC_pap1tOzgTkCr99VbT9k'

    # Redis hosts
    REDIS_HOST = 'localhost'

    # Redis ports
    REDIS_PORT = 6379

    # Redis config
    REDIS_CONFIG = {'host': REDIS_HOST, 'port': REDIS_PORT, 'db': 0}


class TestConfig(BaseConfig):
    TESTING = True
    CSRF_ENABLED = False
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + INSTANCE_FOLDER_PATH + '/test.sqlite'
