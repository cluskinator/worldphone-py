# -*- coding: utf-8 -*-
"""
    theworldphone.modules.call.constants
    ~~~~~~~~~~~~~~~~

    call module constants and enumerables
"""

from enum import Enum


class CallType(Enum):
    # __order__ = 'random exchange'
    random = 1
    exchange = 2
    # tefl = 3


class FlagType(Enum):
    # __order__ = 'verbal sexual other'
    verbal = 1
    sexual = 2
    other = 3

DEFAULT_TOPICS = [
    'traveling',
    'music',
    'art',
    'Formula 1',
    'photography',
    'school',
    'my city',
    'global politics',
    'World Cup',
    'David Bowie',
    'fashion',
    'designs',
    'sports',
    'the Olympics'
]

DEFAULT_TRENDS = [
    '#AddGoatRuinAQuote',
    '#FurnitureASong',
    '#GameOfThrones',
    '#IDontGenerally',
    '#Kanye',
    '#lemons',
    '#MyJobDescriptionIn5Words',
    '#robotics',
    '#TheMuppets',
    '#ThingsThatIForget'
]

# Location for Twitter trends
WOEID = 23424977  # United States

EXCHANGE = 0
RANDOM = 1
TEFL = 2
CALL_TYPES = {
    EXCHANGE: u'EXCHANGE',
    RANDOM: u'RANDOM',
    TEFL: u'TEFL',
}

VERBAL = 0
SEXUAL = 1
OTHER = 2
FLAG_TYPES = {
    VERBAL: u'VERBAL',
    SEXUAL: u'SEXUAL',
    OTHER: u'OTHER'
}
