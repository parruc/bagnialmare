from django.views.generic.edit import CreateView

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
