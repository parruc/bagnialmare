from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
        '',
        url(r"^booking-unsubscribe/$", views.booking_unsubscribe_view, name="booking_unsubscribe"),
)