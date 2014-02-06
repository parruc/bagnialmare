import ast
from itertools import chain

from django import forms
from django.forms.util import flatatt
from django.utils.html import conditional_escape
from django.utils.encoding import StrAndUnicode, force_unicode
from django.utils.safestring import mark_safe
from bagni.models import Bagno, Service
from django.contrib.gis.forms import ModelForm, OSMWidget
from modeltranslation.fields import TranslationField
from modeltranslation.translator import translator


class OmbrelloniOLWidget(OSMWidget):
    #TODO: this thing does not work ... shit
    class Media:
        js = ('http://cdnjs.cloudflare.com/ajax/libs/openlayers/2.11/OpenLayers.min.js',)


class CheckboxInput(forms.widgets.SubWidget):
    """
    An object used by CheckboxRenderer that represents a single
    <input type='checkbox'>.
    """
    def __init__(self, name, value, attrs, choice, index):
        self.name, self.value = name, value
        self.attrs = attrs
        self.choice_value = force_unicode(choice[1])
        self.choice_label = force_unicode(choice[2])

        self.attrs.update({'cat_name': choice[0]})

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

    def __init__(self, *args, **kwargs):
        # Override the default renderer if we were passed one.
        renderer = kwargs.pop('renderer', None)
        if renderer:
            self.renderer = renderer
        super(CheckboxSelectMultipleIter, self).__init__(*args, **kwargs)

    def subwidgets(self, name, value, attrs=None, choices=()):
        for widget in self.get_renderer(name, value, attrs, choices):
            yield widget

    def get_renderer(self, name, value, attrs=None, choices=()):
        """Returns an instance of the renderer."""

        choices_ = [ast.literal_eval(i[1]).iteritems() for i in self.choices]
        choices_ = [(a[1], b[1], c[1]) for a, b, c in choices_]

        if value is None: value = ''
        str_values = set([force_unicode(v) for v in value]) # Normalize to string.
        if attrs is None:
            attrs = {}
        if 'id' not in attrs:
            attrs['id'] = name
        final_attrs = self.build_attrs(attrs)
        choices = list(chain(choices_, choices))
        return self.renderer(name, str_values, final_attrs, choices)

    def render(self, name, value, attrs=None, choices=()):
        return self.get_renderer(name, value, attrs, choices).render()

    def id_for_label(self, id_):
        if id_:
            id_ += '_0'
        return id_


class TranslationModelFormReversed(forms.ModelForm):
    """
    Exactly like from modeltranslation.forms.TranslationModelForm
    but hides base field instead of translated ones.
    """
    def __init__(self, *args, **kwargs):
        super(TranslationModelFormReversed, self).__init__(*args, **kwargs)
        trans_opts = translator.get_options_for_model(Bagno)
        untranslated = trans_opts.fields.keys()
        for f in self._meta.model._meta.fields:
            if f.name not in self.fields and f.name in trans_opts.fields:
                # Removes translated fields not present in fields (in excluded?)
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
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all().values('slug', 'name', 'category__name'),
        widget=CheckboxSelectMultipleIter,
        required=False,
    )
    class Meta:
        model = Bagno
        exclude = ['slug']
        widgets = {'point' : OSMWidget(),}
