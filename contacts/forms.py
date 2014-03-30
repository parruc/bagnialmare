from django import forms
from django.utils.translation import ugettext_lazy as _


class ContactForm(forms.Form):
    sender = forms.EmailField(label=_('Your email address'),
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(max_length=100, label=_('Subject'),
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label=_('Message'),
        widget=forms.Textarea(attrs={'class': 'form-control'}))

    cc_myself = forms.BooleanField(required=False,
        label=_('Send a copy to your address'), initial=True)
