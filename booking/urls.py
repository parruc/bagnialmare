from django.urls import path
from . import views

urlpatterns = [
        path("booking-unsubscribe", views.booking_unsubscribe_view, name="booking_unsubscribe"),
]