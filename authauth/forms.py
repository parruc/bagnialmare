from django.utils.datastructures import MultiValueDict, MergeDict
from django.utils.translation import ugettext_lazy as _

from django import forms

from .models import Manager

class M2MSelect(forms.Select):
    def value_from_datadict(self, data, files, name):
        if isinstance(data, (MultiValueDict, MergeDict)):
            return data.getlist(name)
        return data.get(name, None)


# Create the form class.
class ManagerSignupForm(forms.ModelForm):
    class Meta:
        model = Manager
        fields = ['bagni', 'privacy']
        widgets = {
            'bagni': M2MSelect()
        }

    def save(self, user):
        m = Manager.objects.create(user=user)
        m.bagni = self.cleaned_data['bagni']
        m.privacy = self.cleaned_data['privacy']
        m.save()

    def clean_privacy(self):
        data = self.cleaned_data['privacy']
        if not data:
            raise forms.ValidationError(
                _(u'You must accept the terms and conditions'),
                code='privacy'
            )
        return data
