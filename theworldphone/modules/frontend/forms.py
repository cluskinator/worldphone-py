# -*- coding: utf-8 -*-
"""
    theworldphone.modules.frontend.forms
    ~~~~~~~~~~~~~~~~

    frontend module forms
"""

import uuid

from flask import Markup
from flask.ext.wtf import Form
from flask.ext.wtf.html5 import EmailField
from wtforms import (ValidationError, BooleanField, TextField, SelectField,
    SelectMultipleField, HiddenField, PasswordField, SubmitField)
from wtforms.validators import (AnyOf, Required, Optional, Length, EqualTo, Email)
from flask.ext.babel import lazy_gettext as _

from theworldphone.utils import (PASSWORD_LEN_MIN, PASSWORD_LEN_MAX, USERNAME_LEN_MIN,
    USERNAME_LEN_MAX)
from theworldphone.extensions import db
from theworldphone.modules.user import User, LANGUAGES, COUNTRY_CODES, ACTIVE, GENDER_TYPE


def get_country_code(value):
    for code, fullname in COUNTRY_CODES.items():
        if fullname == value:
            return code


class LoginForm(Form):
    next = HiddenField()
    login = TextField(_('Username or Email'), [Required()])
    password = PasswordField(_('Password'),
        [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)])
    remember = BooleanField(_('Remember me'))
    submit = SubmitField(_('Sign in'))


class SignupForm(Form):
    next = HiddenField()
    email = EmailField(_('Email'), [Required(), Email()],
            description=_("What's your email address?"))
    name = TextField(_('Choose your username'),
        [Required(), Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)])
    location = TextField(_('Location'), [Required()])
    agree = BooleanField(_('I agree ') +
        Markup(_('to the ') + '<a target="blank" href="/terms">' + _('Terms of Service') + '</a>'),
        [Optional()])
    submit = SubmitField('Sign up')

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first() is not None:
            raise ValidationError(_('This username is taken'))

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError(_('This email is taken'))

    def validate_location(self, field):
        if field.data not in COUNTRY_CODES.values():
            raise ValidationError(_('Please choose a valid location.'))

    def signup(self):
        user = User()
        self.location.data = get_country_code(self.location.data)
        self.populate_obj(user)
        user.password = uuid.uuid4().hex
        db.session.add(user)
        db.session.commit()
        return user


class RecoverPasswordForm(Form):
    email = EmailField(_('Your email'), [Email()])
    submit = SubmitField(_('Send instructions'))


class ChangePasswordForm(Form):
    activation_key = HiddenField()
    password = PasswordField(_('Password'), [Required()])
    password_again = PasswordField(_('Confirm'),
        [EqualTo('password', message="Passwords don't match")])
    submit = SubmitField(_('Save'))


class VerifyEmailForm(Form):
    activation_key = HiddenField()
    password = PasswordField(_('Password'), [Required()])
    password_again = PasswordField(_('Confirm'),
        [EqualTo('password', message="Passwords don't match")])
    gender_code = SelectField(_("I am a..."),
        [AnyOf([str(val) for val in GENDER_TYPE.keys()])],
        choices=[(str(val), label) for val, label in GENDER_TYPE.items()])
    source_langs = SelectMultipleField(_('I speak...'),
        choices=[(str(val), label) for val, label in LANGUAGES.items()])
    target_langs = SelectMultipleField(_('I want to learn...'), coerce=str,
        choices=[(str(val), label) for val, label in LANGUAGES.items()])
    submit = SubmitField(_('Verify Login'))

    def validate_source_langs(form, field):
        if field.data is None or len(field.data) < 1:
            raise ValidationError(_('You must select at least one language.'))
        field.data = ";".join(field.data)

    def validate_target_langs(form, field):
        if field.data is None or len(field.data) < 1:
            raise ValidationError(_('You must select at least one language.'))
        elif set(form.source_langs.data) & set(field.data):
            raise ValidationError(_('Sorry. Your source and target language lists must be unique.'))
        field.data = ";".join(field.data)

    def verify(self, user):
        self.populate_obj(user)
        user.change_password(self.password.data)
        user.status_code = ACTIVE
        db.session.commit()
        return user


class ReauthForm(Form):
    next = HiddenField()
    password = PasswordField(_('Password'),
        [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)])
    submit = SubmitField(_('Reauthenticate'))
