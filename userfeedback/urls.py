from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserFeedbackFormView.as_view(), name="user-feedback-form",),
]
