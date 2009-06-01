from django.conf import settings

AUTOLOAD_PREFS_FOR_SYSTEM = getattr(settings, 'AUTOLOAD_PREFS_FOR_SYSTEM', True)