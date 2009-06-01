from django import forms
from models import Pref
from wrapper import preferences

from django.forms.forms import get_declared_fields, BaseForm
from django.forms.widgets import media_property
from django.utils.datastructures import SortedDict

def fields_for_app(app, fields, exclude, owner_class):
    """
    Returns a ``SortedDict`` containing form fields for the given model.

    ``fields`` is an optional list of field names. If provided, only the named
    fields will be included in the returned fields.

    ``exclude`` is an optional list of field names. If provided, the named
    fields will be excluded from the returned fields, even if they are listed
    in the ``fields`` argument.
    """
    field_list = []
    try:
        _app = __import__(app, globals(), locals(), ['prefs'])
        app_prefs = _app.prefs
    except:
        pass
    else:
        default_prefs = getattr(app_prefs, 'for_system', {})
        if owner_class is not None:
            default_prefs.update(getattr(app_prefs, 'for_owner', {}).get(owner_class, {}))
        for name, field in default_prefs.items():
            if fields and not name in fields:
                continue
            if exclude and name in exclude:
                continue
            if field:
                field_list.append((name, field))
    field_dict = SortedDict(field_list)
    if fields:
        field_dict = SortedDict([(f, field_dict.get(f)) for f in fields if (not exclude) or (exclude and f not in exclude)])
    return field_dict

class PrefFormOptions(object):
    
    def __init__(self, options=None):
        self.app = getattr(options, 'app', None)
        self.verbose_name = getattr(options, 'verbose_name', None)
        self.fields = getattr(options, 'fields', None)
        self.exclude = getattr(options, 'exclude', None)
        self.owner_class = getattr(options, 'owner_class', None)


class PrefFormMetaclass(type):
    
    def __new__(cls, name, bases, attrs):
        try:
            parents = [b for b in bases if issubclass(b, PrefForm)]
        except NameError:
            # We are defining PrefForm itself.
            parents = None
        declared_fields = get_declared_fields(bases, attrs, False)
        new_class = super(PrefFormMetaclass, cls).__new__(cls, name, bases, attrs)
        if not parents:
            return new_class

        if 'media' not in attrs:
            new_class.media = media_property(new_class)
        opts = new_class._meta = PrefFormOptions(getattr(new_class, 'Meta', None))
        if opts.app:
            # If an app is defined, extract form fields from it.
            fields = fields_for_app(opts.app, opts.fields,
                                      opts.exclude, opts.owner_class)
            # Override default model fields with any custom declared ones
            # (plus, include all the other declared fields).
            fields.update(declared_fields)
        else:
            fields = declared_fields
        new_class.declared_fields = declared_fields
        new_class.base_fields = fields
        return new_class


class BasePrefForm(BaseForm):
    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop('owner', None)
        self.pref_filter = Pref.get_filter(self.owner)
        super(BasePrefForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            try:
                field.initial = preferences.get(field_name, owner=self.owner, default=field.initial)
            except AttributeError:
                pass

    def save(self, commit=True):
        for key, value in self.cleaned_data.items():
            if value is not None:
                preferences.set(key, value, owner=self.owner)
            else:
                preferences.remove(key, owner=self.owner)
        return self.cleaned_data


class PrefForm(BasePrefForm):
    __metaclass__ = PrefFormMetaclass
