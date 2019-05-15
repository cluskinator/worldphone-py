# -*- coding: utf-8 -*-
"""
    theworldphone.modules.admin.forms
    ~~~~~~~~~~~~~~~~

    admin module forms
"""

from flask.ext.wtf import Form
from wtforms import (HiddenField, SubmitField, SelectField, FileField, DateField)
from wtforms.validators import AnyOf

from theworldphone.extensions import db
from theworldphone.modules.user.constants import UserStatus


class UserForm(Form):
    next = HiddenField()
    status = SelectField(u"Status", [AnyOf([str(s.name) for s in UserStatus])],
            choices=[(str(s.name), s.name.capitalize()) for s in UserStatus])
    created_time = DateField(u'Created time')  # _created_at ?
    submit = SubmitField(u'Save')

    def save(self, user):
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()


class EditTranslationForm(Form):
    multipart = True
    file = FileField(u"Upload Translation File")
    language = HiddenField()
    submit = SubmitField(u'Save')
