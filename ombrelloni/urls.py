from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

# Uncomment the next two lines to enable the admin:
from django.contrib.gis import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^i18n/', include('multilingual.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

)

urlpatterns += i18n_patterns(
    '',
    # Bagni urls
    url(r'^', include('bagni.urls')),

    # Authentication initial path
    url(_(r'^accounts/'), include('allauth.urls')),
)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
    url(r'^__debug__/', include(debug_toolbar.urls)),
)
