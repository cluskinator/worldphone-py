# -*- coding: utf-8 -*-
"""
    theworldphone.logger
    ~~~~~~~~~~~~~~~~

    theworldphone logger module
"""

from inspect import currentframe, getframeinfo
from datetime import datetime
import logging

from flask import request
from flask.ext.login import current_user


class LogAdapter(logging.LoggerAdapter):
    def __init__(self, logger, extra={}):
        super(LogAdapter, self).__init__(logger, extra)

        for lvl in ['critical', 'error', 'warning', 'info', 'debug']:
            if self.logger.isEnabledFor(lvl):
                self.add_level(lvl)

    def process(self, msg, lvl, kwargs):
        level = ("%s:" % lvl.upper()).ljust(10)
        return """%(timestamp)s (UTC)
%(file_context)s
%(lvl)s %(msg)s
%(user_context)s""" % {
            'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'file_context': self.file_context(),
            'lvl': level,
            'msg': msg,
            'user_context': self.user_context()
        }, kwargs

    def add_level(self, lvl):
        def lvl_fn(msg, *args, **kwargs):
            """
            Delegate a {lvl} call to the underlying logger, after adding
            contextual information from this adapter instance.
            """
            args = ()
            kwargs = {}
            msg, kwargs = self.process(msg, lvl, kwargs)
            getattr(self.logger, lvl)(msg, *args, **kwargs)
        setattr(self, lvl, lvl_fn)

    def file_context(self):
        # (here) < self.process:21 < self.debug/info/error:32/40/48 < log_exception:78/79 < call it
        frameinfo = getframeinfo(currentframe().f_back.f_back.f_back.f_back)
        return "[%s:%s]" % (frameinfo.filename, frameinfo.lineno)

    def user_context(self):
        user = '%s <%s>' % (
            getattr(current_user, 'fullname', 'anonymous'),
            getattr(current_user, 'email', 'NONE'))
        agent = "%s | %s %s" % (
            request.user_agent.platform, request.user_agent.browser, request.user_agent.version)

        return """Request:   %(method)s %(path)s
IP:        %(ip)s
User:      %(user)s
Agent:     %(agent)s
Raw Agent: %(raw_agent)s
        """ % {
            'method': request.method,
            'path': request.path,
            'ip': request.remote_addr,
            'user': user,
            'agent': agent,
            'raw_agent': request.user_agent.string
        }


def log_exception(exception):
    LogAdapter(logging.getLogger('theworldphone')).error(exception)
