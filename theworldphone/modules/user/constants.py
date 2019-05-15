# -*- coding: utf-8 -*-
"""
    theworldphone.modules.user.constants
    ~~~~~~~~~~~~~~~~

    user module constants and enumerables
"""

from enum import Enum


class UserStatus(Enum):
    # __order__ = 'new active inactive banned'
    new = 1
    active = 2
    inactive = 3
    banned = 4


class Gender(Enum):
    # __order__ = 'male female other'
    male = 1
    female = 2
    other = 3


class RatingType(Enum):
    # __order__ = 'overall grammar vocabulary accent skill'
    overall = 1
    grammar = 2
    vocabulary = 3
    accent = 4


class UserRole(Enum):
    # __order__ = 'admin user tefl_pending tefl tefl_denied'
    admin = 1
    user = 2
    tefl_pending = 3
    tefl = 4
    tefl_denied = 5

MALE = 0
FEMALE = 1
OTHER = 2

GENDER_TYPE = {
    MALE: 'Male',
    FEMALE: 'Female',
    OTHER: 'Other'
}

# User role
ADMIN = 0
USER = 1
TEFL_PENDING = 2
TEFL = 3
TEFL_DENIED = 4
USER_ROLE = {
    ADMIN: 'Admin',
    USER: 'User',
    TEFL_PENDING: 'TEFL Pending',
    TEFL: 'TEFL',
    TEFL_DENIED: 'TEFL Denied',
}

# User status
INACTIVE = 0
ACTIVE = 1
BANNED = 2
NEW = 4
USER_STATUS = {
    INACTIVE: 'Inactive',
    ACTIVE: 'Active',
    BANNED: 'Banned',
    NEW: 'New'
}

ENGLISH = 0
SPANISH = 1
FRENCH = 2
GERMAN = 3
JAPANESE = 4
CHINESE = 5
TURKISH = 6
RUSSIAN = 7
ARABIC = 8
PORTUGUESE = 9
LANGUAGES = {
    ENGLISH: u'ENGLISH',
    SPANISH: u'SPANISH',
    FRENCH: u'FRENCH',
    GERMAN: u'GERMAN',
    JAPANESE: u'JAPANESE',
    CHINESE: u'CHINESE',
    TURKISH: u'TURKISH',
    RUSSIAN: u'RUSSIAN',
    ARABIC: u'ARABIC',
    PORTUGUESE: u'PORTUGUESE'
}

TOPICS = {
    'ENGLISH': [
        'soccer',
        'music',
        'Disney movies',
        'Nickelback',
        'art',
        'your city',
        'food',
        'your family',
        'life dreams',
        'video games',
        'pop culture',
        'the world',
        'Europe',
        'the Kardashians',
    ],

    'SPANISH': [
        'fútbol',
        'música',
        'las películas de Disney',
        'Nickelback',
        'arte',
        'tu ciudad',
        'comida',
        'su familia',
        'planes de futuro',
        'juegos de vídeo',
        'la cultura pop',
        'el mundo',
        'Europa',
        'los Kardashians',
    ],

    'FRENCH': [
        'football',
        'musique',
        'films de Disney',
        'Nickelback',
        'art',
        'votre ville',
        'nourriture',
        'votre famille',
        'les plans futurs',
        'jeux vidéo',
        'la culture pop',
        'Monde',
        'Europe',
        'les Kardashians',
    ],

    'GERMAN': [
        'Fußball',
        'Musik',
        'Disney-Filme',
        'Nickelback',
        'Kunst',
        'Ihre Stadt',
        'Lebensmittel',
        'Ihre Familie',
        'Zukunftspläne',
        'videospiele',
        'Popkultur',
        'die Welt',
        'Europa',
        'die Kardashians',
    ],

    'JAPANESE': [
        'サッカー',
        '音楽',
        'ディズニー映画',
        'Nickelback',
        'アート',
        'あなたの都市',
        '食べ物',
        'あなたの家族',
        '今後の計画',
        'ビデオゲーム',
        'ポップカルチャー',
        '世界',
        'ヨーロッパ',
        'Kardashiansに',
    ],

    'CHINESE': [
        '足球',
        '音樂',
        '迪斯尼電影',
        'Nickelback',
        '藝術',
        '您所在的城市',
        '食品',
        '你的家人',
        '未來計劃',
        '視頻遊戲',
        '流行文化',
        '世界',
        '歐洲',
        'the Kardashians',
    ],

    'TURKISH': [
        'futbol',
        'müzik',
        'Disney filmleri',
        'Nickelback',
        'sanat',
        'Şehrinizi',
        'gıda',
        'aileniz',
        'gelecek planları',
        'video oyunları',
        'pop kültürü',
        'Dünya',
        'Avrupa',
        'Kardashian',
    ],

    'RUSSIAN': [
        'футбол',
        'музыка',
        'фильмы Диснея',
        'Nickelback',
        'искусство',
        'ваш город',
        'еда',
        'семья',
        'планы на будущее',
        'видеоигры',
        'поп-культура',
        'Мир',
        'Европа',
        'в Kardashians',
    ],

    'ARABIC': [
        'لعبة كرة القدم',
        'موسيقى',
        'أفلام ديزني',
        'Nickelback',
        'فن',
        'مدينتك',
        'غذاء',
        'عائلتك',
        'أحلام الحياة',
        'ألعاب الفيديو',
        'ثقافة البوب',
        'العالم',
        'أوروبا',
        'وKardashians',
    ],

    'PORTUGUESE': [
        'futebol',
        'música',
        'filmes da Disney',
        'Nickelback',
        'arte',
        'sua cidade',
        'comida',
        'sua família',
        'planos futuros',
        'jogos de vídeo',
        'cultura pop',
        'mundo',
        'Europa',
        'os Kardashians',
    ],

}

COUNTRY_CODES = {
    'AD': u"Andorra",
    'AE': u"United Arab Emirates",
    'AF': u"Afghanistan",
    'AG': u"Antigua and Barbuda",
    'AI': u"Anguilla",
    'AL': u"Albania",
    'AM': u"Armenia",
    'AO': u"Angola",
    'AQ': u"Antarctica",
    'AR': u"Argentina",
    'AS': u"American Samoa",
    'AT': u"Austria",
    'AU': u"Australia",
    'AW': u"Aruba",
    'AX': u"Åland Islands",
    'AZ': u"Azerbaijan",
    'BA': u"Bosnia and Herzegovina",
    'BB': u"Barbados",
    'BD': u"Bangladesh",
    'BE': u"Belgium",
    'BF': u"Burkina Faso",
    'BG': u"Bulgaria",
    'BH': u"Bahrain",
    'BI': u"Burundi",
    'BJ': u"Benin",
    'BL': u"Saint Barthélemy",
    'BM': u"Bermuda",
    'BN': u"Brunei Darussalam",
    'BO': u"Bolivia, Plurinational State of",
    'BQ': u"Bonaire, Sint Eustatius and Saba",
    'BR': u"Brazil",
    'BS': u"Bahamas",
    'BT': u"Bhutan",
    'BV': u"Bouvet Island",
    'BW': u"Botswana",
    'BY': u"Belarus",
    'BZ': u"Belize",
    'CA': u"Canada",
    'CC': u"Cocos (Keeling) Islands",
    'CD': u"Congo (the Democratic Republic of the)",
    'CF': u"Central African Republic",
    'CG': u"Congo",
    'CH': u"Switzerland",
    'CI': u"Côte d'Ivoire",
    'CK': u"Cook Islands",
    'CL': u"Chile",
    'CM': u"Cameroon",
    'CN': u"China",
    'CO': u"Colombia",
    'CR': u"Costa Rica",
    'CU': u"Cuba",
    'CV': u"Cabo Verde",
    'CW': u"Curaçao",
    'CX': u"Christmas Island",
    'CY': u"Cyprus",
    'CZ': u"Czech Republic",
    'DE': u"Germany",
    'DJ': u"Djibouti",
    'DK': u"Denmark",
    'DM': u"Dominica",
    'DO': u"Dominican Republic",
    'DZ': u"Algeria",
    'EC': u"Ecuador",
    'EE': u"Estonia",
    'EG': u"Egypt",
    'EH': u"Western Sahara*",
    'ER': u"Eritrea",
    'ES': u"Spain",
    'ET': u"Ethiopia",
    'FI': u"Finland",
    'FJ': u"Fiji",
    'FK': u"Falkland Islands [Malvinas]",
    'FM': u"Micronesia (the Federated States of)",
    'FO': u"Faroe Islands",
    'FR': u"France",
    'GA': u"Gabon",
    'GB': u"United Kingdom",
    'GD': u"Grenada",
    'GE': u"Georgia",
    'GF': u"French Guiana",
    'GG': u"Guernsey",
    'GH': u"Ghana",
    'GI': u"Gibraltar",
    'GL': u"Greenland",
    'GM': u"Gambia",
    'GN': u"Guinea",
    'GP': u"Guadeloupe",
    'GQ': u"Equatorial Guinea",
    'GR': u"Greece",
    'GS': u"South Georgia and the South Sandwich Islands",
    'GT': u"Guatemala",
    'GU': u"Guam",
    'GW': u"Guinea-Bissau",
    'GY': u"Guyana",
    'HK': u"Hong Kong",
    'HM': u"Heard Island and McDonald Islands",
    'HN': u"Honduras",
    'HR': u"Croatia",
    'HT': u"Haiti",
    'HU': u"Hungary",
    'ID': u"Indonesia",
    'IE': u"Ireland",
    'IL': u"Israel",
    'IM': u"Isle of Man",
    'IN': u"India",
    'IO': u"British Indian Ocean Territory",
    'IQ': u"Iraq",
    'IR': u"Iran (the Islamic Republic of)",
    'IS': u"Iceland",
    'IT': u"Italy",
    'JE': u"Jersey",
    'JM': u"Jamaica",
    'JO': u"Jordan",
    'JP': u"Japan",
    'KE': u"Kenya",
    'KG': u"Kyrgyzstan",
    'KH': u"Cambodia",
    'KI': u"Kiribati",
    'KM': u"Comoros",
    'KN': u"Saint Kitts and Nevis",
    'KP': u"Korea (the Democratic People's Republic of)",
    'KR': u"Korea (the Republic of)",
    'KW': u"Kuwait",
    'KY': u"Cayman Islands",
    'KZ': u"Kazakhstan",
    'LA': u"Lao People's Democratic Republic",
    'LB': u"Lebanon",
    'LC': u"Saint Lucia",
    'LI': u"Liechtenstein",
    'LK': u"Sri Lanka",
    'LR': u"Liberia",
    'LS': u"Lesotho",
    'LT': u"Lithuania",
    'LU': u"Luxembourg",
    'LV': u"Latvia",
    'LY': u"Libya",
    'MA': u"Morocco",
    'MC': u"Monaco",
    'MD': u"Moldova (the Republic of)",
    'ME': u"Montenegro",
    'MF': u"Saint Martin (French part)",
    'MG': u"Madagascar",
    'MH': u"Marshall Islands",
    'MK': u"Macedonia (the former Yugoslav Republic of)",
    'ML': u"Mali",
    'MM': u"Myanmar",
    'MN': u"Mongolia",
    'MO': u"Macao",
    'MP': u"Northern Mariana Islands",
    'MQ': u"Martinique",
    'MR': u"Mauritania",
    'MS': u"Montserrat",
    'MT': u"Malta",
    'MU': u"Mauritius",
    'MV': u"Maldives",
    'MW': u"Malawi",
    'MX': u"Mexico",
    'MY': u"Malaysia",
    'MZ': u"Mozambique",
    'NA': u"Namibia",
    'NC': u"New Caledonia",
    'NE': u"Niger",
    'NF': u"Norfolk Island",
    'NG': u"Nigeria",
    'NI': u"Nicaragua",
    'NL': u"Netherlands",
    'NO': u"Norway",
    'NP': u"Nepal",
    'NR': u"Nauru",
    'NU': u"Niue",
    'NZ': u"New Zealand",
    'OM': u"Oman",
    'PA': u"Panama",
    'PE': u"Peru",
    'PF': u"French Polynesia",
    'PG': u"Papua New Guinea",
    'PH': u"Philippines",
    'PK': u"Pakistan",
    'PL': u"Poland",
    'PM': u"Saint Pierre and Miquelon",
    'PN': u"Pitcairn",
    'PR': u"Puerto Rico",
    'PS': u"Palestine, State of",
    'PT': u"Portugal",
    'PW': u"Palau",
    'PY': u"Paraguay",
    'QA': u"Qatar",
    'RE': u"Réunion",
    'RO': u"Romania",
    'RS': u"Serbia",
    'RU': u"Russian Federation",
    'RW': u"Rwanda",
    'SA': u"Saudi Arabia",
    'SB': u"Solomon Islands",
    'SC': u"Seychelles",
    'SD': u"Sudan",
    'SE': u"Sweden",
    'SG': u"Singapore",
    'SH': u"Saint Helena, Ascension and Tristan da Cunha",
    'SI': u"Slovenia",
    'SJ': u"Svalbard and Jan Mayen",
    'SK': u"Slovakia",
    'SL': u"Sierra Leone",
    'SM': u"San Marino",
    'SN': u"Senegal",
    'SO': u"Somalia",
    'SR': u"Suriname",
    'SS': u"South Sudan",
    'ST': u"Sao Tome and Principe",
    'SV': u"El Salvador",
    'SX': u"Sint Maarten (Dutch part)",
    'SY': u"Syrian Arab Republic",
    'SZ': u"Swaziland",
    'TC': u"Turks and Caicos Islands",
    'TD': u"Chad",
    'TF': u"French Southern Territories",
    'TG': u"Togo",
    'TH': u"Thailand",
    'TJ': u"Tajikistan",
    'TK': u"Tokelau",
    'TL': u"Timor-Leste",
    'TM': u"Turkmenistan",
    'TN': u"Tunisia",
    'TO': u"Tonga",
    'TR': u"Turkey",
    'TT': u"Trinidad and Tobago",
    'TV': u"Tuvalu",
    'TW': u"Taiwan (Province of China)",
    'TZ': u"Tanzania, United Republic of",
    'UA': u"Ukraine",
    'UG': u"Uganda",
    'UM': u"United States Minor Outlying Islands",
    'US': u"United States",
    'UY': u"Uruguay",
    'UZ': u"Uzbekistan",
    'VA': u"Holy See [Vatican City State]",
    'VC': u"Saint Vincent and the Grenadines",
    'VE': u"Venezuela, Bolivarian Republic of ",
    'VG': u"Virgin Islands (British)",
    'VI': u"Virgin Islands (U.S.)",
    'VN': u"Viet Nam",
    'VU': u"Vanuatu",
    'WF': u"Wallis and Futuna",
    'WS': u"Samoa",
    'YE': u"Yemen",
    'YT': u"Mayotte",
    'ZA': u"South Africa",
    'ZM': u"Zambia",
    'ZW': u"Zimbabwe"
}
