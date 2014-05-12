from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    '',
    url(r'^$',
        views.UserFeedbackFormView.as_view(),
        name="user-feedback-form",),
)
