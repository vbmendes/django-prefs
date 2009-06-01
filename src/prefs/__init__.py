from constants import *
from wrapper import preferences
from settings import AUTOLOAD_PREFS_FOR_SYSTEM
from django.conf import settings
from forms import fields_for_app

if AUTOLOAD_PREFS_FOR_SYSTEM:
    for app in settings.INSTALLED_APPS:
        fields = fields_for_app(app, None, None, None)
        for name, field in fields.items():
            preferences.get(name, autoset=field.initial)