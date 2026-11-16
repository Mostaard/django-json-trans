from unittest import TestCase
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.db.models import JSONField

from src.json_trans.models import MultiLanguageField


class TranslationTest(TestCase):
    def test_validate_correct_language_code(self):
        field = MultiLanguageField()
        validated = field.validate_language_code('fr')
        self.assertTrue(validated)

    def test_validate_incorrect_language_code(self):
        field = MultiLanguageField()
        with self.assertRaises(ValidationError):
            field.validate_language_code('frans')

    def test_validate_translation_value_not_string(self):
        field = MultiLanguageField()
        with self.assertRaises(ValidationError):
            field.validate_translation('fr', {
                'default': 'fr',
                'translations': {
                    'fr': 4
                }
            })

    def test_validate_schema(self):
        """"""
        field = MultiLanguageField()
        with self.assertRaises(ValidationError):
            field.validate({'something'}, None)

    def test_validate_value_without_translations(self):
        field = MultiLanguageField()
        for value in ({}, {'default': 'nl'}, {'translations': {'nl': 'Nederlands'}}):
            with self.subTest(value=value), self.assertRaises(ValidationError):
                field.validate(value, None)

    def test_validate_accepts_a_text_per_language(self):
        field = MultiLanguageField()
        field.validate({'default': 'nl', 'translations': {'nl': 'Nederlands', 'en': 'English'}}, None)

    @patch.object(JSONField, 'validate', autospec=True)
    def test_validate_value_with_no_translations_reaches_json_field(self, json_validate):
        field = MultiLanguageField()
        field.validate({'default': 'nl', 'translations': {}}, None)
        json_validate.assert_called_once()

    @patch.object(JSONField, 'validate', autospec=True)
    def test_validate_value_with_three_languages_reaches_json_field_once(self, json_validate):
        field = MultiLanguageField()
        field.validate({'default': 'nl', 'translations': {'nl': 'Nederlands', 'en': 'English', 'fr': 'Français'}},
                       None)
        json_validate.assert_called_once()
