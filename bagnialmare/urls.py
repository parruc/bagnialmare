from django.urls import path, re_path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from django.utils.translation import ugettext_lazy as _

# Uncomment the next two lines to enable the admin:
from django.contrib.gis import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.auth.views import LogoutView
from bagnialmare.common.sitemaps import get_sitemaps

SITEMAPS = get_sitemaps(['bagni', 'contacts'])

admin.autodiscover()


urlpatterns = [
    # Uncomment the admin/doc line below to enable admin documentation:
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('i18n/', include('multilingual.urls')),
    # Uncomment the next line to enable the admin:
    path('admin/', admin.site.urls),
    #enables the sitemaps framework
    path('sitemap.xml', sitemap, {'sitemaps': SITEMAPS}, name='django.contrib.sitemaps.views.sitemap'),
    #enables rich text editing
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

urlpatterns += i18n_patterns(
    # Bagni urls
    path('', include('bagni.urls')),
    re_path(_(r'^contacts/'), include('contacts.urls')),
    re_path(_(r'^newsletters/'), include('newsletters.urls')),
    #exclude logout confirmation step
    re_path(r'^accounts/logout/$', LogoutView.as_view(), {'next_page': '/'}, name='django.contrib.auth.views.logout'),
    # Authauth rewrites signup view
    re_path(_(r'^accounts/'), include('authauth.urls')),
    # Authentication initial path
    re_path(_(r'^accounts/'), include('allauth.urls')),
    re_path(_(r'^userfeedback/'), include('userfeedback.urls')),
    re_path(_(r'^booking/'), include('booking.urls')),
    prefix_default_language=True,
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [ path('__debug__/', include(debug_toolbar.urls)), ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
