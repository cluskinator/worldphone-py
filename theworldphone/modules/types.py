# -*- coding: utf-8 -*-
"""
    theworldphone.modules.types
    ~~~~~~~~~~~~~~~~

    custom SQLAlchemy column type extensions
"""

from sqlalchemy import types
from sqlalchemy.ext.mutable import Mutable


class DenormalizedText(Mutable, types.TypeDecorator):
    """
    Stores denormalized primary keys that can be accessed as a set.

    :param coerce: coercion function that ensures correct type is returned
    :param separator: separator character
    """

    impl = types.Text

    def __init__(self, coerce=int, separator=" ", **kwargs):

        self.coerce = coerce
        self.separator = separator

        super(DenormalizedText, self).__init__(**kwargs)

    def process_bind_param(self, value, dialect):
        if value is not None:
            items = [str(item).strip() for item in value]
            value = self.separator.join(item for item in items if item)
        return value

    def process_result_value(self, value, dialect):
        if not value:
            return set()
        return set(self.coerce(item) for item in value.split(self.separator))

    def copy_value(self, value):
        return set(value)


class MutableDict(Mutable, dict):
    """
    Implement a mutable dict that is pickled and stored in the database

    :method coerce: coercion function that ensures correct type is returned
    :method __delitem:
    :method __getstate__:
    :method __setstate__:
    """
    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, MutableDict):
            if isinstance(value, dict):
                return MutableDict(value)
            return Mutable.coerce(key, value)
        else:
            return value

    def __delitem(self, key):
        dict.__delitem__(self, key)
        self.changed()

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        self.changed()

    def __getstate__(self):
        return dict(self)

    def __setstate__(self, state):
        self.update(self)
