from models import Pref
from django.contrib.auth.models import User
from django.conf import settings
from meio.utils import CREATED, UPDATED
from constants import CASCADE_ALL

class PrefsWrapper:
    
    def __getattr__(self, name):
        return self.get(name)

    def __setattr__(self, name, value):
        return self.set(name, value)
    
    def __delattr__(self, name):
        return self.remove(name)
    
    def get(self, key, owner=None, default=None, autoset=None, autoset_for_system=False, cascade=CASCADE_ALL):
        for_system = owner is None
        if not for_system or not key in self.__dict__:
            try:
                value = Pref.objects.get_value(
                    key,
                    owner=owner,
                    default=default,
                    autoset=autoset,
                    autoset_for_system=autoset_for_system,
                    cascade=cascade
                )
                if for_system or autoset_for_system:
                    self.__dict__[key] = value
                return value
            except Pref.DoesNotExist:
                raise AttributeError("System has no preference '%s'")
        return self.__dict__[key]
    
    def set(self, key, value, owner=None):
        for_system = owner is None
        if for_system and key in self.__dict__:
            self.__dict__[key] = value
        query = Pref.objects.filter(key=key, **Pref.get_filter(owner))
        if query.count() > 0:
            pref = query.get()
            pref.value = value
            pref.save()
            return UPDATED
        else:
            if owner:
                Pref(key=key, owner=owner, value=value).save()
            else:
                Pref(key=key, for_system=True, value=value).save()
            return CREATED
    
    def remove(self, key, owner=None):
        for_system = owner is None
        if for_system:
            self.__dict__.pop(key,None)
        try:
            Pref.objects.get(key=key, **Pref.get_filter(owner)).delete()
            return True
        except Pref.DoesNotExist:
            return False


preferences = PrefsWrapper()