# -*- coding: utf-8 -*-
from django.urls import re_path
from django.utils.translation import ugettext_lazy as _

from . import views

urlpatterns = [
    re_path(_(r'^subscribe/(?P<slug>[-\w]+)/(?P<email>[\w.%+-_]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$'), views.SubscribeNewsletter.as_view(), name="newsletter-subscribe"),
    re_path(_(r'^unsubscribe/(?P<hash>[\w]+)/$'), views.UnsubscribeNewsletter.as_view(), name="newsletter-unsubscribe"),
]
