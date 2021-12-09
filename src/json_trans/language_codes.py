from enum import Enum

class LanguageCode(Enum):
    ARABIC = "ar"
    BULGARIAN = "bg"
    CHINESE = "zh"
    DANISH = "da"
    DUTCH = "nl"
    ENGLISH = 'en'
    FINNISH = "fi"
    FRENCH = 'fr'
    GERMAN = 'deu'
    GREEK = 'ell'
    HUNGARIAN = 'hun'
    ITALIAN = 'ita'
    JAPANESE = 'jpn'
    NORWEGIAN = 'nor'
    POLISH = 'pol'
    PORTUGUESE = 'por'
    ROMANIAN = 'rum'
    RUSSIAN = 'rus'
    SPANISH = 'spa'
    SWEDISH = 'swe'
    TURKISH = 'tur'

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)

    def __str__(self):
        return self.value

