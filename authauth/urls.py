from django.urls import path
from . import views

urlpatterns = [
        path("signup/", views.ManagerSignupView.as_view(), name="authauth_signup"),
]
