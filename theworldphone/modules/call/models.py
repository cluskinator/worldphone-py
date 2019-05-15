# -*- coding: utf-8 -*-
"""
    theworldphone.modules.call.models
    ~~~~~~~~~~~~~~~~

    call models
"""

from sqlalchemy import Column, or_
from marshmallow_jsonapi import Schema, fields
from marshmallow import validate

from time import mktime, strptime
from datetime import datetime

from theworldphone.extensions import db
from theworldphone.modules.base import Base
from theworldphone.modules.types import MutableDict
from theworldphone.modules.user.models import Language, LanguageSchema
from theworldphone.utils import STRING_LEN

from .constants import CallType


class CallLog(Base):
    """
        CallLog class. Contains information about both call participants and the call settings.

        :param string account_sid: (AccountSid)
        :param string app_sid: (ApplicationSid)
        :param string call_sid: (CallSid)
        :param int call_type: Enum (random, exchange)
        :param int caller_uid: uid of the caller
        :param int callee_uid: uid of the callee
        :param string caller_ip: ip address of caller
        :param string callee_ip: ip address of callee
        :param string caller_username: username of caller
        :param string callee_username: username of callee
        :param string language1_uid: uid of first call language
        :param string language2_uid: uid of second call language
        :param datetime start_time: time the call started
        :param string status: call status (DialCallStatus)
        :param string recording_sid:
        :param int recording_duration:
        :param string recording_url:
        :param bool flagged:
        :param dict comment:
    """

    account_sid = Column(db.String(STRING_LEN))
    app_sid = Column(db.String(STRING_LEN))
    call_sid = Column(db.String(STRING_LEN))
    caller_uid = Column(db.String(STRING_LEN), db.ForeignKey('user.uid'))
    callee_uid = Column(db.String(STRING_LEN), db.ForeignKey('user.uid'))
    caller_ip = Column(db.String(STRING_LEN))
    callee_ip = Column(db.String(STRING_LEN))
    caller_username = Column(db.String(STRING_LEN))
    callee_username = Column(db.String(STRING_LEN))
    caller_quality = Column(db.Integer)
    callee_quality = Column(db.Integer)
    status = Column(db.String(STRING_LEN))
    start_time = Column(db.DateTime)
    end_time = Column(db.DateTime)
    recording_sid = Column(db.String(STRING_LEN))
    recording_duration = Column(db.Integer)
    recording_url = Column(db.String(150))
    flagged = Column(db.Boolean, default=False)
    comments = Column(MutableDict.as_mutable(db.PickleType), default=dict())  # { user_id : comment}

    language1_uid = Column(db.String(STRING_LEN), db.ForeignKey(Language.uid), nullable=True)
    language1 = db.relationship(Language, foreign_keys='CallLog.language1_uid')
    language2_uid = Column(db.String(STRING_LEN), db.ForeignKey(Language.uid), nullable=True)
    language2 = db.relationship(Language, foreign_keys='CallLog.language2_uid')

    _call_type_code = Column(db.SmallInteger, default=CallType['random'].value)

    @property
    def call_type(self):
        return CallType(self._call_type_code).name

    @call_type.setter
    def call_type(self, call_type_name):
        self._call_type_code = CallType[call_type_name].value

    @property
    def duration(self):
        if self.start_time and self.end_time:
            total = (self.end_time - self.start_time).total_seconds()
            h = int(total // 3600)
            m = int(total % 3600 // 60)
            s = int(total % 60)
            return '{:02}:{:02}:{:02}'.format(h, m, s)

    def with_user(self, user_uid):
        return CallLog.query.filter(
            CallLog.end_time != None,
            or_(CallLog.caller_uid == user_uid, CallLog.callee_uid == user_uid))

    def completed(self):
        return CallLog.query.filter(CallLog.end_time != None)

    def add_comment(self, user_id, text, flags):
        self.comments[user_id] = (text, flags)
        self.flagged = True

    def remove_comment(self, user_id):
        if user_id in self.comments:
            del self.comments[user_id]
        if len(self.comments) == 0:
            self.flagged = False

    @staticmethod
    def queue_name(call_type, languages):
        q = 'r' if call_type == 'random' else 'ex'
        for language in languages:
            q += '_%s' % language
        return q


class CallLogSchema(Schema):
    id = fields.UUID(dump_only=True, attribute='uid', required=True)
    account_sid = fields.String()
    app_sid = fields.String()
    call_sid = fields.String()
    call_type = fields.String()
    caller_uid = fields.String()
    callee_uid = fields.String()
    caller_ip = fields.String()
    callee_ip = fields.String()
    caller_username = fields.String()
    callee_username = fields.String()
    caller_quality = fields.Integer()
    callee_quality = fields.Integer()
    language1 = fields.Nested(LanguageSchema)
    language2 = fields.Nested(LanguageSchema)
    start_time = fields.DateTime()
    end_time = fields.DateTime()
    duration = fields.String(dump_only=True)
    status = fields.String()
    # recording_sid = fields.String()
    # recording_duration = fields.Integer()
    # recording_url = fields.String()
    flagged = fields.Boolean(dump_only=True)
    # comments = fields.()

    class Meta:
        type_ = 'call_log'
