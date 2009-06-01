from django.db import models
from queryset import PrefQuerySet
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
import pickle

class Pref(models.Model):
    key = models.CharField(max_length=255)
    pickled_value = models.TextField()
    for_system = models.BooleanField()
    owner_type = models.ForeignKey(ContentType, null=True, blank=True)
    owner_id = models.PositiveIntegerField(null=True, blank=True)
    owner = generic.GenericForeignKey('owner_type', 'owner_id')
    created = models.DateTimeField(auto_now_add=True)
    
    objects = PrefQuerySet.as_manager()

    class Meta:
        ordering = ('key',)
        verbose_name = u'preference'
        verbose_name_plural = u'preferences'

    def __init__(self, *args, **kwargs):
        if 'value' in kwargs:
            self.value = kwargs.pop('value')
        super(Pref, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return self.key
    
    def save(self, *args, **kwargs):
        self.for_system = self.owner is None
        self.pickled_value = pickle.dumps(self.value)
        if self.owner is None:
            self.owner = User.objects.all()[0]
            self.owner_type = ContentType.objects.get_for_model(self.owner)
            self.owner_id = self.owner.pk
        super(Pref, self).save(*args, **kwargs)
        
    @staticmethod
    def get_filter(owner):
        if owner is None:
            return { 'for_system': True }
        else:
            owner_type = ContentType.objects.get_for_model(owner)
            return { 'owner_type': owner_type, 'owner_id': owner.pk }

    def get_value(self):
        if not hasattr(self, '_value'):
            self._value = pickle.loads(str(self.pickled_value))
        return self._value
    
    def set_value(self, value):
        self._value = value
    
    value = property(get_value, set_value)
