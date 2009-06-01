# In case a object's preference is requested
# and it does not exist. Don't look in system
# preferences.
CASCADE_NONE = 0

# In case a object's preference is requested
# and it does not exist, then search for a 
# system preference with the same key.
CASCADE_SYSTEM  = 1

# In case a system preference is requested and
# it does not exist, the search for a setting
# (in settings.py) with the same key.
CASCADE_SETTINGS = 2

CASCADE_ALL = 1000

FOR_SYSTEM = None
