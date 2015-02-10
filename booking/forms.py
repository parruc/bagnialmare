from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ("bagno", "created", "modified", )

    start = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d'),
                            input_formats=('%Y-%m-%d',))
    end = forms.DateField(widget=forms.DateInput(format='%Y-%M-%d',
                                                 attrs={"class":"date-control"}),
                          input_formats=('%Y-%M-%d',))
