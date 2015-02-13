from datetime import date
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ("created", "modified", )

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        # change a widget attribute:
        classes = "form-control date-control"
        input_formats = (_('%m/%d/%Y'), )
        self.fields['start'].widget.attrs["class"] = classes
        self.fields['end'].widget.attrs["class"] = classes
        self.fields['start'].widget.input_formats = input_formats
        self.fields['end'].widget.input_formats = input_formats
        self.fields['umbrellas'].min_value = 0
        self.fields['sunbeds'].min_value = 0

    def clean(self):
        cleaned_data = super(BookingForm, self).clean()
        start = cleaned_data.get("start", date.today())
        end = cleaned_data.get("end", date.today())
        if start > end:
            error_msg = _("'To' must be equal or greater than 'From'")
            raise ValidationError(error_msg)
        self.cleaned_data = cleaned_data
        return cleaned_data

    def clean_start(self):
        start = self.cleaned_data['start']
        if start < date.today():
            error_msg = _("'From' must be equal or greater than today")
            raise ValidationError(error_msg)
        return start

    def clean_end(self):
        end = self.cleaned_data['end']
        if end < date.today():
            error_msg = _("'To' must be equal or greater than today")
            raise ValidationError(error_msg)
        return end
