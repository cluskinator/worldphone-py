# -*- coding: utf-8 -*-
"""
    gunicorn.py
    ~~~~~~~~~~~~~~~~

    gunicorn configuration
"""

import os

bind = '0.0.0.0:' + os.environ.get('PORT', '5000')

loglevel = 'error'
logger_class = 'simple'
accesslog = 'tmp/instance/logs/gunicorn/access.log'
errorlog = 'tmp/instance/logs/gunicorn/error.log'
logfile = 'tmp/instance/logs/gunicorn/gunicorn.log'

backlog = 2048
