# -*- coding: utf-8 -*-
"""
    theworldphone.modules.user.models
    ~~~~~~~~~~~~~~~~

    user models
"""

import uuid

from sqlalchemy import Column
from marshmallow_jsonapi import Schema, fields
from marshmallow import validate
from werkzeug import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin

from theworldphone.extensions import db
from theworldphone.modules.base import Base
from theworldphone.modules.types import MutableDict
from theworldphone.utils import STRING_LEN

from .constants import UserRole, UserStatus, Gender, RatingType


spoken_languages = db.Table(
    'spoken_languages',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('language_id', db.Integer, db.ForeignKey('language.id'))
)

learning_languages = db.Table(
    'learning_languages',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('language_id', db.Integer, db.ForeignKey('language.id'))
)


class User(Base, UserMixin):
    """
        User class.  Covers all roles, including ADMIN and TEFL

        :auth0_user_id string auth0_user_id: Auth0 user id
        :param string name: Name
        :param string email: E-mail
        :param string activation_key: Used for verify e-mail / forget password stuff
        :param string location: Two-character country code
        :param dict _ip_list:  Looks like: [time] = 'ip_address'
        :param int _gender_code: Enum (male, female, other)
        :param string _password: Accessed using password = db.synonym('_password')
        :param int _role_code: Enum (admin, user, tefl_pending, tefl, tefl_denied)
        :param int _status_code: Enum (new, active, inactive, banned)
    """

    auth0_user_id = Column(db.String(STRING_LEN), nullable=False, unique=True)
    name = Column(db.String(STRING_LEN), nullable=False)
    email = Column(db.String(STRING_LEN), nullable=False, unique=True)
    activation_key = Column(db.String(STRING_LEN))
    location = Column(db.String(STRING_LEN))
    _ip_list = Column(MutableDict.as_mutable(db.PickleType), default=dict())

    # 1:M relationship via M:M structure
    spoken_languages = db.relationship('Language', secondary=spoken_languages)
    learning_languages = db.relationship('Language', secondary=learning_languages)

    _gender_code = Column(db.Integer)

    @property
    def gender(self):
        if self._gender_code:
            return Gender(self._gender_code).name

    @gender.setter
    def gender(self, gender_name):
        if gender_name:
            self._gender_code = Gender[gender_name].value

    # password
    _password = Column('password', db.String(STRING_LEN))

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = generate_password_hash(password)

    # Hide password encryption by exposing password field only.
    password = db.synonym('_password', descriptor=property(_get_password, _set_password))

    def check_password(self, password):
        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    def reset_password(self):
        self.activation_key = uuid.uuid4().hex
        db.session.add(self)
        db.session.commit()

    def change_password(self, passwd):
        self.password = passwd
        self.activation_key = None
        db.session.add(self)
        db.session.commit()

    # role code
    _role_code = Column(db.SmallInteger, default=UserRole.user.value)

    @property
    def role(self):
        return UserRole(self._role_code).name

    @role.setter
    def role(self, role_name):
        if role_name:
            self._role_code = UserRole[role_name].value

    def is_admin(self):
        return self.role == 'admin'

    def is_tefl_pending(self):
        return self.role == 'tefl_pending'

    def is_tefl(self):
        return self.role == 'tefl'

    def no_tefl(self):
        return not (self.role == 'tefl' or
            self.role == 'tefl_pending' or
            self.role == 'tefl_denied')

    def tefl_denied(self):
        return self.role == 'tefl_denied'

    # status code
    _status_code = Column(db.SmallInteger, default=UserStatus.new.value)

    @property
    def status(self):
        return UserStatus(self._status_code).name

    @status.setter
    def status(self, status_name):
        self._status_code = UserStatus[status_name].value

    # User ratings (1:M relationship)
    ratings = db.relationship('Rating', lazy='dynamic')

    def init_ratings(self):
        for rating_type in RatingType:
            rating = Rating(_type_code=rating_type.value)
            self.ratings.append(rating)
            Rating().save(rating)

    def set_ratings(self, new_values):
        self.add_overall(new_values.get('overall'))
        self.add_grammar(new_values.get('grammar'))
        self.add_vocabulary(new_values.get('vocabulary'))
        self.add_accent(new_values.get('accent'))

    def get_rating(self, rating_name):
        return Rating().first(user_id=self.id, _type_code=RatingType[rating_name].value)

    # Individual ratings (not set directly)

    @property
    def overall(self):
        return self.get_rating('overall')

    def add_overall(self, new_value):
        return self.overall.add_value(new_value)

    @property
    def grammar(self):
        return self.get_rating('grammar')

    def add_grammar(self, new_value):
        return self.grammar.add_value(new_value)

    @property
    def vocabulary(self):
        return self.get_rating('vocabulary')

    def add_vocabulary(self, new_value):
        return self.vocabulary.add_value(new_value)

    @property
    def accent(self):
        return self.get_rating('accent')

    def add_accent(self, new_value):
        return self.accent.add_value(new_value)

    # Miscellaneous

    def update_languages(self, spoken_uids, learning_uids):
        languages = Language().all()
        for language in languages:
            if language.uid in spoken_uids and language not in self.spoken_languages:
                self.spoken_languages.append(language)
            elif language in self.spoken_languages and language.uid not in spoken_uids:
                self.spoken_languages.remove(language)
            if language.uid in learning_uids and language not in self.learning_languages:
                self.learning_languages.append(language)
            elif language in self.learning_languages and language.uid not in learning_uids:
                self.learning_languages.remove(language)
        return User().save(self)

    # Like a relationship, but not really...
    @property
    def call_logs(self):
        return CallLog().with_user(self.uid)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'gender': self.gender,
            'overall': self.overall_rating,
            'tefl': self.is_tefl()
        }

    @classmethod
    def authenticate(cls, login, password):
        user = cls.query.filter(db.or_(User.name == login, User.email == login)).first()
        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False
        return user, authenticated

    def check_name(self, name):
        return User.query.filter(db.and_(User.name == name, User.email != self.id)).count() == 0


class Rating(Base):
    """
        Rating class. Uses cumulative moving averages

        :param int _type_code: Enum (overall, grammar, vocabulary, accent, skill)
        :param float average: Current average
        :param int n: Number of values making up average
    """

    average = Column(db.Float(3), nullable=False, default=0.0)
    n = Column(db.Integer, nullable=False, default=0)
    user_id = Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User, backref=db.backref('rating', cascade='all'))  # cascade='delete' ?

    _type_code = Column(db.Integer, nullable=False)

    @property
    def type(self):
        return RatingType(self._type_code).name

    @type.setter
    def type(self, type_name):
        self._type_code = RatingType[type_name].value

    def add_value(self, new_rating):
        if new_rating:
            new_value = (new_rating - 1) * 25.0  # convert 1-5 stars to 0.0-100.0 (0-4 * 25.0)
            self.average = self.average + (new_value - self.average) / (self.n + 1)
            self.n += 1
            return Rating().update(self)  # should it save here, or just return self?

    def stars(self):
        # convert 0.0-100.0 average to 1-5 stars
        return (self.average / 25.0) + 1


class Language(Base):
    """
        Language class

        :param string name: Language name as string
    """
    name = Column(db.String(STRING_LEN), nullable=False)


class RatingSchema(Schema):
    id = fields.UUID(dump_only=True, attribute='uid', required=True)
    type = fields.String()
    average = fields.Float(dump_only=True)
    n = fields.Integer(dump_only=True)

    class Meta:
        type_ = 'rating'


class LanguageSchema(Schema):
    id = fields.UUID(dump_only=True, attribute='uid', required=True)
    name = fields.String(required=True)

    class Meta:
        type_ = 'language'


class UserSchema(Schema):
    # not_blank = validate.Length(min=1, error='Field cannot be blank')
    id = fields.UUID(dump_only=True, attribute='uid', required=True)
    auth0_user_id = fields.String(dump_only=True)
    name = fields.String()  # nickname?
    email = fields.String()
    location = fields.String()
    gender = fields.String()
    status = fields.String()
    created_at = fields.Date(dump_only=True, attribute='_created_at')
    updated_at = fields.Date(dump_only=True, attribute='_updated_at')
    spoken_languages = fields.Nested(LanguageSchema, many=True)
    learning_languages = fields.Nested(LanguageSchema, many=True)
    ratings = fields.Nested(RatingSchema, dump_only=True, many=True)

    # self links
    def get_top_level_links(self, data, many):
        return {'self': "/users/{}".format(data['id'])}

    class Meta:
        type_ = 'user'
