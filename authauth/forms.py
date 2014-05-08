from django.utils.datastructures import MultiValueDict, MergeDict
from django.utils.translation import ugettext_lazy as _

from django import forms

from .models import Manager
import logging
logger = logging.getLogger(__name__)

class M2MSelect(forms.Select):
    def value_from_datadict(self, data, files, name):
        if isinstance(data, (MultiValueDict, MergeDict)):
            return data.getlist(name)
        return data.get(name, None)


# Create the form class.
class ManagerSignupForm(forms.ModelForm):
    class Meta:
        model = Manager
        fields = ['name', 'surname', 'bagni', 'privacy', 'tos']
        widgets = {
            'bagni': M2MSelect(),
            'name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'surname' : forms.TextInput(attrs={'class' : 'form-control'}),
            'email' : forms.TextInput(attrs={'class' : 'form-control'}),
        }

    def signup(self, request, user):
        user.first_name = self.cleaned_data['name']
        user.last_name = self.cleaned_data['surname']
        m = Manager.objects.create(user=user)
        m.bagni = self.cleaned_data['bagni']
        m.privacy = self.cleaned_data['privacy']
        m.name = self.cleaned_data['name']
        m.surname = self.cleaned_data['surname']
        m.save()

    def _clean_required_bool(self, field_name):
        data = self.cleaned_data[field_name]
        if not data:
            raise forms.ValidationError(
                _(u'You must accept the terms and conditions'),
                code='privacy'
            )
        return data

    def clean_privacy(self):
        return self._clean_required_bool('privacy')

    def clean_tos(self):
        return self._clean_required_bool('tos')
