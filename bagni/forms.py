from itertools import chain

from django import forms
from django.forms.util import flatatt
from django.forms.models import inlineformset_factory, ModelFormMetaclass
from django.utils.html import conditional_escape
from django.utils.encoding import StrAndUnicode, force_unicode
from django.utils.safestring import mark_safe
from bagni.models import Bagno, Service, Image, Telephone
from django.contrib.gis.forms import ModelForm, OSMWidget
from django.utils import six

from modeltranslation.translator import translator

import logging
logging.getLogger(__name__)


class OmbrelloniOLWidget(OSMWidget):
    """
    Just Inherits from standard widget in contrib in order to load js files from local static folder
    """

    default_lon = 5
    default_lat = 10
    #template_name = 'gis/openlayers-osm.html'

    class Media:
        extend = False
        js = ('/static/js/OpenLayers-2.11.js',
              '/static/js/OpenStreetMap.js',
              '/static/js/olsetup.js',
              'gis/js/OLMapWidget.js')
        css = {
                'all' : ('/static/css/openlayers.tidy.css',),
              }

class CheckboxInput(forms.widgets.SubWidget):
    """
    An object used by CheckboxRenderer that represents a single
    <input type='checkbox'>.
    """
    def __init__(self, name, value, attrs, choice, index):
        self.name, self.value = name, value
        self.attrs = attrs
        self.choice_value = force_unicode(choice[0])
        self.choice_label = force_unicode(choice[1])
        self.attrs.update({'cat_name': choice[2]})
        self.index = index

    def __unicode__(self):
        return self.render()

    def render(self, name=None, value=None, attrs=None, choices=()):
        name = name or self.name
        value = value or self.value
        attrs = attrs or self.attrs

        if 'id' in self.attrs:
            label_for = ' for="%s_%s"' % (self.attrs['id'], self.index)
        else:
            label_for = ''
        choice_label = conditional_escape(force_unicode(self.choice_label))
        return mark_safe(u'<label%s>%s %s</label>' % (label_for, self.tag(), choice_label))

    def is_checked(self):
        return self.choice_value in self.value

    def tag(self):
        if 'id' in self.attrs:
            self.attrs['id'] = '%s_%s' % (self.attrs['id'], self.index)
        final_attrs = dict(self.attrs, type='checkbox', name=self.name, value=self.choice_value)
        if self.is_checked():
            final_attrs['checked'] = 'checked'
        return mark_safe(u'<input%s />' % flatatt(final_attrs))


class CheckboxRenderer(StrAndUnicode):
    def __init__(self, name, value, attrs, choices):
        self.name, self.value, self.attrs = name, value, attrs
        self.choices = choices

    def __iter__(self):
        for i, choice in enumerate(self.choices):
            yield CheckboxInput(self.name, self.value, self.attrs.copy(), choice, i)

    def __getitem__(self, idx):
        choice = self.choices[idx] # Let the IndexError propogate
        return CheckboxInput(self.name, self.value, self.attrs.copy(), choice, idx)

    def __unicode__(self):
        return self.render()

    def render(self):
        """Outputs a <ul> for this set of checkbox fields."""
        return mark_safe(u'<ul>\n%s\n</ul>' % u'\n'.join([u'<li>%s</li>'
                % force_unicode(w) for w in self]))


class CheckboxSelectMultipleIter(forms.CheckboxSelectMultiple):
    """
    Checkbox multi select field that enables iteration of each checkbox
    Similar to django.forms.widgets.RadioSelect
    """
    renderer = CheckboxRenderer

    def get_renderer(self, name, value, attrs=None, choices=()):
        """Returns an instance of the renderer."""

        choices_ = [(c.pk, c.name, c.category.name) for c in self.choices.queryset]

        if value is None: value = ''
        str_values = set([force_unicode(v) for v in value]) # Normalize to string.
        if attrs is None:
            attrs = {}
        if 'id' not in attrs:
            attrs['id'] = name
        final_attrs = self.build_attrs(attrs)
        choices = list(chain(choices_, choices))
        return self.renderer(name, str_values, final_attrs, choices)


class TranslationModelFormMetaclass(ModelFormMetaclass):
    def __new__(cls, name, bases, attrs):
        meta = attrs.get('Meta', None)
        #if the class has an inner class called Meta
        if meta:
            #we store the names of translated attributes in the inner class Meta
            setattr(meta, 'translations', [])
            #if the inner class Meta defines a fields attribute
            meta_fields = getattr(meta, 'fields', None)
            if meta_fields:
                trans_opts = translator.get_options_for_model(meta.model)
                translations = trans_opts.fields.keys()
                # if the attribute is listed in Meta.fields (must be added to the form)
                for field in meta_fields:
                    #if this attribute supports translation
                    if field in translations:
                        #save the position of this field in the form
                        position = meta_fields.index(field)
                        #remove base field before adding its translations
                        meta_fields.pop(position)
                        #add tanslated fields
                        for t_field in trans_opts.fields[field]:
                            meta_fields.insert(position, t_field.name)
                            meta.translations.append(t_field.name)
        return super(TranslationModelFormMetaclass, cls).__new__(cls, name, bases, attrs)


class TranslationModelForm(six.with_metaclass(TranslationModelFormMetaclass, ModelForm)):
    def __init__(self, *args, **kwargs):
        super(TranslationModelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.iteritems():
            if field_name in self.Meta.translations:
                # This field is relative to a translation.
                # You can add your code here to customize the translated fields.
                css_class = "field-trans-%s" % field_name
                setattr(field, "css_class", css_class)


class TelephoneForm(TranslationModelForm):
    class Meta:
        model = Telephone
        fields = ['name',
                  'number',
                  ]


class ImageForm(TranslationModelForm):
    class Meta:
        model = Image
        fields = ['name',
                  'description',
                  'image',
                  ]


# These two are used with extra_views package
#class TelephoneInline(InlineFormSet):
#    model = Telephone
#    form_class = TelephoneForm
#
#class ImageInline(InlineFormSet):
#    model = Image
#    form_class = ImageForm

# These two are used by our own defined BagnoEdit view
TelephoneFormSet = inlineformset_factory(Bagno, Telephone, form=TelephoneForm)
ImageFormSet = inlineformset_factory(Bagno, Image, form=ImageForm)

class BagnoForm(TranslationModelForm):

    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.select_related("category__name").all(),
        widget=CheckboxSelectMultipleIter,
        required=False,
    )

    class Meta:
        model = Bagno
        # the order matters here!
        fields = [
                  'name',
                  'description',
                  'number',
                  'address',
                  'languages',
                  'services',
                  'municipality',
                  'mail',
                  'site',
                  'point',
                  ]

        widgets = {'point' : OmbrelloniOLWidget(),}




