import logging
from enum import Enum
from gettext import gettext as _

import pycountry
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import JSONField
from jsonschema import validate
from jsonschema.exceptions import ValidationError as JSONSchemaError

logger = logging.getLogger(__name__)

LANGUAGE_CODES = [language.alpha_2 for language in pycountry.languages if
                  hasattr(language, 'alpha_2')]

schema = {
    'type': 'object',
    'properties': {
        'default': {'type': 'string'},
        'translations': {'type': 'object'},
    }

}


class ErrorCode(Enum):
    LANGUAGE_CODE = 'LANGUAGE_CODE'
    TRANSLATION = 'TRANSLATION'

    def __str__(self):
        return self.value


class MultiLanguageField(JSONField):
    def validate(self, value, model_instance):
        self.validate_schema(value)
        for language_code in value['translations'].keys():
            self.validate_language_code(language_code)
            self.validate_translation(language_code, value)
            super().validate(value, model_instance)

    @staticmethod
    def validate_schema(value):
        try:
            validate(value, schema)
        except JSONSchemaError:
            raise ValidationError(
                message=_(
                    f"{value} is of a incompatible schema with MultiLanguageField "),
                code=ErrorCode.TRANSLATION,
            )

    @staticmethod
    def validate_translation(language_code: str, value: dict) -> bool:
        if not isinstance(value['translations'].get(language_code), str):
            raise ValidationError(
                message=_(
                    '{} is an invalid translation'.format(value.get(language_code))),
                code=ErrorCode.TRANSLATION,
            )
        return True

    @staticmethod
    def validate_language_code(language_code: str) -> bool:
        language_code_list = [language for language in
                              dict(
                                  settings.LANGUAGES)] if settings.configured and settings.LANGUAGES else LANGUAGE_CODES
        if language_code not in language_code_list:
            raise ValidationError(
                message=_(
                    'Language with code {} is not supported'.format(language_code)),
                code=ErrorCode.LANGUAGE_CODE,
            )
        return True


def get_translated_value(field, language_code=''):
    if not field:
        return field
    if not isinstance(field, dict):
        return str(field)
    if not language_code or language_code not in field['translations'].keys():
        language_code = field['default']
    try:
        return field['translations'][language_code]
    except (KeyError, TypeError):
        logger.error(
            '{} - missing translation for language code {} in jsonfield {}'.format(
                str(ErrorCode.TRANSLATION),
                str(language_code), field))
        return 'NO TRANSLATION AVAILABLE'
