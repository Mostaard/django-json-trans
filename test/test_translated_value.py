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

    def test_get_translated_value_missing_default_translation_is_empty(self):
        field = {
            'default': 'nl',
            'translations': {
                'en': 'English',
            }
        }
        with self.assertLogs('src.json_trans.models', level='ERROR'):
            self.assertEqual(get_translated_value(field, 'fr'), '')

    def test_get_translated_value_non_dict_field_returns_string(self):
        field = 1
        self.assertEqual(get_translated_value(field, 'fr'), '1')

    def test_get_translated_value_empty_value_is_empty(self):
        for field in (None, {}):
            with self.subTest(field=field):
                self.assertEqual(get_translated_value(field, 'fr'), '')

    def test_get_translated_value_without_default(self):
        field = {'translations': {'en': 'English'}}
        self.assertEqual(get_translated_value(field, 'en'), 'English')
        with self.assertLogs('src.json_trans.models', level='ERROR'):
            self.assertEqual(get_translated_value(field, 'fr'), '')

    def test_get_translated_value_without_translations(self):
        for field in ({'default': 'nl'}, {'default': 'nl', 'translations': None}):
            with self.subTest(field=field), self.assertLogs('src.json_trans.models', level='ERROR'):
                self.assertEqual(get_translated_value(field, 'nl'), '')
