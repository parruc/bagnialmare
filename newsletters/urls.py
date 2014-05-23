# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import views
from django.utils.translation import ugettext_lazy as _

urlpatterns = patterns(
    '',
    url(_(r'^subscribe/(?P<slug>[-\w]+)/(?P<email>[\w.%+-_]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$'), views.SubscribeNewsletter.as_view(), name="newsletter-subscribe"),
    url(_(r'^unsubscribe/(?P<hash>[\w]+)/$'), views.UnsubscribeNewsletter.as_view(), name="newsletter-unsubscribe"),
)
