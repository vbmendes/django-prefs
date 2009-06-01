from django.conf import settings
from meio.db.models.query import QuerySet
from constants import CASCADE_NONE, CASCADE_SYSTEM, CASCADE_SETTINGS, CASCADE_ALL

class PrefQuerySet(QuerySet):

    def get_value(self, key, owner=None, default=None, autoset=None, autoset_for_system=False, cascade=CASCADE_ALL):
        if autoset is not None and default is not None:
            raise ValueError("Can't use default and autoset parameters at the same time.")
        # creating arguments for Pref search or creation, based in owner and for_system parameters
        pref_filter = self.model.get_filter(owner)
        for_system = owner is None
        try:
            return self.get(key=key, **pref_filter).value
        except self.model.DoesNotExist:
            if cascade > CASCADE_SYSTEM:
                if owner:
                    try:
                        return self.get(key=key, for_system=True).value
                    except self.model.DoesNotExist:
                        pass
                if cascade > CASCADE_SETTINGS:
                    try:
                        return getattr(settings, key)
                    except AttributeError:
                        pass
            if autoset is not None:
                if for_system or autoset_for_system:
                    self.model(key=key, value=autoset, for_system=True).save()
                else:
                    self.model(key=key, value=autoset, owner=owner).save()
                return autoset
            elif default is not None:
                return default
            raise