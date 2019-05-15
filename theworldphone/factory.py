# -*- coding: utf-8 -*-
"""
    theworldphone.factory
    ~~~~~~~~~~~~~~~~

    application factory
"""

import os, logging
import logging.handlers as handlers

from flask import Flask, request, render_template, jsonify
from flask.ext.babel import Babel

from theworldphone.config import DefaultConfig
from theworldphone.core.logger import log_exception

from theworldphone.modules.api import api
from theworldphone.modules.admin import admin
from theworldphone.modules.call import call
from theworldphone.modules.call.services import call_log
from theworldphone.modules.mailchimp import chimp
from theworldphone.modules.frontend import frontend
from theworldphone.modules.user import User, user

from theworldphone.extensions import db, cache, login_manager
from theworldphone.utils import INSTANCE_FOLDER_PATH, PROJECT_PATH


# For import *
__all__ = ['create_app']


DEFAULT_BLUEPRINTS = (
    frontend,
    admin,
    call,
    chimp,)

API_BLUEPRINTS = (
    api,
    call_log,
    user,)


def create_app(config=None, app_name=None, blueprints=None):
    """Create a Flask app."""
    if app_name is None:
        app_name = DefaultConfig.PROJECT
    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(app_name, instance_path=INSTANCE_FOLDER_PATH, instance_relative_config=True)
    configure_app(app, config)
    configure_blueprints(app, blueprints)
    configure_api_blueprints(app, API_BLUEPRINTS)
    configure_extensions(app)
    configure_template_filters(app)
    configure_hook(app)
    configure_logging(app)
    configure_error_handlers(app)

    return app


def configure_app(app, config=None):
    # http://flask.pocoo.org/docs/api/#configuration
    app.config.from_object(DefaultConfig)

    # If config is None, try to load config file from environment variable
    if config is None and 'FBONE_CFG' in os.environ:
        app.config.from_envvar('FBONE_CFG')

    # pass configuration file in with application manager
    if config:
        config_file = os.path.join(PROJECT_PATH, config)
        app.config.from_pyfile(config_file, silent=False)


def configure_extensions(app):
    # flask-sqlalchemy
    db.init_app(app)

    # flask-cache
    cache.init_app(app)

    # flask-babel
    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(DefaultConfig.LANGUAGES)

    # flask-login
    login_manager.login_view = 'admin.login'
    login_manager.refresh_view = 'admin.reauth'

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)
    login_manager.setup_app(app)


def configure_blueprints(app, blueprints):
    """Configure blueprints in views."""
    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def configure_api_blueprints(app, blueprints):
    """Configure blueprints in views."""
    for blueprint in blueprints:
        app.register_blueprint(blueprint, url_prefix='/api/v1')


def configure_template_filters(app):

    @app.template_filter()
    def pretty_date(value):
        return pretty_date(value)

    @app.template_filter()
    def format_date(value, format='%Y-%m-%d'):
        return value.strftime(format)

    @app.template_filter()
    def local_tz(utc_datetime):
        from dateutil import tz

        dt = utc_datetime.replace(tzinfo=tz.tzutc())
        return dt.astimezone(tz.tzlocal()).strftime('%m/%d/%y %I:%M %p')

    # jinja globals
    # app.jinja_env.globals.update()


def configure_logging(app):
    """Configure file(info) and email(error) logging."""
    # Skip during tests.
    if app.config['TESTING']:
        return

    # Set info level on logger, which might be overwritten by handlers.
    app.logger.setLevel(logging.INFO)

    log = os.path.join(app.config['LOG_FOLDER'], 'app.log')
    file_handler = handlers.RotatingFileHandler(log, maxBytes=100000, backupCount=10)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    # set logging level(s) for imported modules
    logging.getLogger('sqlalchemy').setLevel(logging.ERROR)


def configure_hook(app):
    pass
    # @app.before_request
    # def before_request():
    #     pass

    # @app.after_request
    # def after_request():
    #     pass

    # @app.context_processor
    # def ctx_processor():
    #     pass


def configure_error_handlers(app):

    @app.errorhandler(404)
    def page_not_found(error):
        log_exception(error)
        if 'api' in request.url:
            resp = jsonify({'status': 404, 'message': 'Not Found: ' + request.url, })
            resp.status_code = 404
            return resp
        return render_template("errors/page_not_found.html"), 404

    @app.errorhandler(403)
    def forbidden_page(error):
        log_exception(error)
        if 'api' in request.url:
            resp = jsonify({'status': 403, 'message': 'Forbidden: ' + request.url, })
            resp.status_code = 403
            return resp
        return render_template("errors/forbidden_page.html"), 403

    @app.errorhandler(500)
    def server_error_page(error):
        log_exception(error)
        if 'api' in request.url:
            resp = jsonify({'status': 500, 'message': 'Internal Server Error: ' + request.url, })
            resp.status_code = 500
            return resp
        return render_template("errors/server_error.html"), 500
