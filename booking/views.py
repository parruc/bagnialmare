from django.core import signing
from django.shortcuts import render
from django.http import Http404
from django.views.generic.edit import CreateView

from bagni.models import Bagno

from .forms import BookingForm

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class BookingView(CreateView):
    form_class = BookingForm
    template_name = "booking/booking.html"


class BookingModalView(BookingView):
    form_class = BookingForm
    template_name = "booking/booking_modal.html"


signer = signing.Signer('s2hdf73as5f')

def booking_unsubscribe_view(request):
    signed_email = request.REQUEST.get('e', '')
    try:
       email = signer.unsign(signed_email)
    except signing.BadSignature:
        raise Http404

    # handle also case of multiple beach resorts sharing the same email
    bagni = Bagno.objects.filter(mail=email)
    if not bagni:
        raise Http404

    if request.method == 'POST':
        for bagno in bagni:
            bagno.accepts_booking = False
            bagno.save()
        return render(request, 'booking/booking_unsubscribe_successful.html')

    return render(request, 'booking/confirm_booking_unsubscribe.html', {'e': signed_email})