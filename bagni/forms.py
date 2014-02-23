from itertools import chain

from django import forms
from django.forms.util import flatatt
from django.forms.models import inlineformset_factory, ModelFormMetaclass, BaseModelForm
from django.utils.html import conditional_escape
from django.utils.encoding import StrAndUnicode, force_unicode
from django.utils.safestring import mark_safe
from bagni.models import Bagno, Service, Image, Telephone
from django.contrib.gis.forms import ModelForm, OSMWidget
from django.utils import six
from modeltranslation.fields import TranslationField
from modeltranslation.translator import translator


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
        new_class = super(TranslationModelFormMetaclass, cls).__new__(cls, name, bases, attrs)
        return new_class

class TranslationModelForm(six.with_metaclass(TranslationModelFormMetaclass, BaseModelForm)):
        pass

class TranslationModelFormReversed(forms.ModelForm):
    """
    Exactly like from modeltranslation.forms.TranslationModelForm
    but hides base field instead of translated ones.
    """
    def __init__(self, *args, **kwargs):
        super(TranslationModelFormReversed, self).__init__(*args, **kwargs)
        trans_opts = translator.get_options_for_model(Bagno)
        untranslated = trans_opts.fields.keys()
        #translations = trans_opts.fields
        for f in self._meta.model._meta.fields:
        #    #if this attribute must be translated and must be included in the form
        #    if f.name in translations and f.name in self.fields:
        #        #save position of this field in the form
        #        position = self.fields.keyOrder.index(f.name)
        #        #remove base fields for translations
        #        #del self.fields[f.name]
        #        #add tanslated fields
        #        for t_field in translations[f.name]:
        #            #add custom class to the field for javascript visualization
        #            css_class = "field-trans-%s" % f.name
        #            t_field.css_class = css_class
        #            # add the translated field in the form in the correct position
        #            # self.fields is an instance of django.utils.SortedDict
        #            self.fields.keyOrder.insert(position, t_field.name)
        #            self.fields[t_field.name] = t_field
            if f.name not in self.fields and f.name in trans_opts.fields:
                # Removes translated fields not present in fields
                for trans_f in trans_opts.fields[f.name]:
                    if trans_f.name in self.fields:
                        del self.fields[trans_f.name]
            if f.name in self.fields:
                if f.name in untranslated:
                    # Removes the fields with a translation
                    del self.fields[f.name]
                if isinstance(f, TranslationField):
                    # Adjusts translated fields
                    css_class = "field-trans-%s" % f.name
                    setattr(self.fields[f.name], "css_class", css_class)


# Create the form class.
class BagnoForm(TranslationModelFormReversed, ModelForm):
#class BagnoForm(TranslationModelForm):

    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.select_related("category__name").all(),
        widget=CheckboxSelectMultipleIter,
        required=False,
    )
    class Meta:
        model = Bagno
        fields = ['name', 'name_en', 'name_it',
                'description', 'description_en', 'description_it',
                'number',
                'address', 'address_en', 'address_it',
                'languages', 'services',
                'municipality', 'mail', 'site', 'point']
        widgets = {'point' : OmbrelloniOLWidget(),}
