from unittest import TestCase

from django.core.exceptions import ValidationError

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
                'fr': 4,
            })

    def test_validate_schema(self):
        """"""
        field = MultiLanguageField()
        with self.assertRaises(ValidationError):
            field.validate({'something'}, None)
