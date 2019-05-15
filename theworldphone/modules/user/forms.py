# -*- coding: utf-8 -*-
"""
    theworldphone.modules.user.forms
    ~~~~~~~~~~~~~~~~

    user module forms
"""

from flask.ext.wtf import Form
from flask.ext.wtf.html5 import EmailField
from flask.ext.babel import lazy_gettext as _
from flask.ext.login import current_user
from wtforms import (ValidationError, HiddenField, PasswordField, SubmitField, SelectField,
    SelectMultipleField)
from wtforms.validators import (Required, Length, EqualTo, Email, AnyOf)


from theworldphone.utils import PASSWORD_LEN_MIN, PASSWORD_LEN_MAX
from theworldphone.extensions import db

from .constants import LANGUAGES, GENDER_TYPE
from .models import User


class ProfileForm(Form):
    multipart = True
    next = HiddenField()
    email = EmailField(_('Email'), [Required(), Email()])
    gender_code = SelectField(_("I am a..."),
        [AnyOf([str(val) for val in GENDER_TYPE.keys()])],
        choices=[(str(val), label) for val, label in GENDER_TYPE.items()])
    location = HiddenField()
    source_langs = SelectMultipleField(_('I speak...'),
        choices=[(str(val), label) for val, label in LANGUAGES.items()])
    target_langs = SelectMultipleField(_('I want to learn...'), coerce=str,
        choices=[(str(val), label) for val, label in LANGUAGES.items()])

    submit = SubmitField(_('Save'))

    def validate_name(form, field):
        user = User.get_by_id(current_user.id)
        if not user.check_name(field.data):
            raise ValidationError(_("Please pick another name."))

    def validate_source_langs(form, field):
        field.data = ";".join(field.data)

    def validate_target_langs(form, field):
        field.data = ";".join(field.data)

    def create_profile(self, request, user):
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()


class PasswordForm(Form):
    next = HiddenField()
    password = PasswordField(_('Current password'), [Required()])
    new_password = PasswordField(_('New password'),
        [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)])
    password_again = PasswordField(_('Password again'),
        [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX), EqualTo('new_password')])
    submit = SubmitField(_('Save'))

    def validate_password(form, field):
        user = User.get_by_id(current_user.id)
        if not user.check_password(field.data):
            raise ValidationError(_("Password is wrong."))

    def update_password(self, user):
        self.populate_obj(user)
        user.password = self.new_password.data

        db.session.add(user)
        db.session.commit()
