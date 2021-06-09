========================
Django JSON Translations
========================

Django JSON Translations is an app that provides a field for storing
translations in PostgreSQL JSON field.


Config
-------

Add the supported languages in settings as following
LANGUAGES = [
('en', _('English')),
('nl', _('Dutch')),
('fr', _('French')),
]

Build
_____
python setup.py sdist
