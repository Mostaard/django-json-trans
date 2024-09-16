from unittest import TestCase

from src.json_trans.models import get_translated_value


class TranslationTest(TestCase):
    def test_get_translated_value_existing_translation(self):
        field = {
            'default': 'nl',
            'translations': {
                'nl': 'Nederlands',
                'en': 'English',
            }
        }
        self.assertEqual(get_translated_value(field, 'en'), 'English')

    def test_get_translated_value_default_translation(self):
        field = {
            'default': 'nl',
            'translations': {
                'nl': 'Nederlands',
                'en': 'English',
            }
        }
        self.assertEqual(get_translated_value(field), 'Nederlands')

    def test_get_translated_value_default_fallback(self):
        field = {
            'default': 'nl',
            'translations': {
                'nl': 'Nederlands',
                'en': 'English',
            }
        }
        self.assertEqual(get_translated_value(field, 'fr'), 'Nederlands')

    def test_get_translated_value_missing_translation(self):
        field = {
            'default': 'nl',
            'translations': {
                'en': 'English',
            }
        }
        self.assertEqual(get_translated_value(field, 'fr'), 'NO TRANSLATION AVAILABLE')

    def test_get_translated_value_non_dict_field_returns_string(self):
        field = 1
        self.assertEqual(get_translated_value(field, 'fr'), '1')
