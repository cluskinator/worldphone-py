# -*- coding: utf-8 -*-
"""
    theworldphone.extensions
    ~~~~~~~~~~~~~~~~

    flask application extensions instantions
"""

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask.ext.cache import Cache
cache = Cache()

from flask.ext.login import LoginManager
login_manager = LoginManager()
