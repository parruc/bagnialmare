from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
        '',
        url(r"^signup/$", views.ManagerSignupView.as_view(), name="authauth_signup"),
)
