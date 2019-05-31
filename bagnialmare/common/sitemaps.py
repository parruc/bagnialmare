from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.utils.translation import activate
from django.urls import reverse
from importlib import import_module

all = ["LocalesSitemap", "StaticLocalesSitemap", "get_sitemaps"]

class LocalesSitemap(Sitemap):
    def get_urls(self, page=1, site=None, protocol=None):
        urls = []
        for lang in settings.LANGUAGES:
            lang_code = lang[0]
            activate(lang_code)
            _urls = super(LocalesSitemap, self).get_urls(page, site, protocol)
            urls.extend(_urls)
        return urls

class StaticLocalesSitemap(LocalesSitemap):
    def location(self, item):
        return reverse(item)

def get_sitemaps(applications):
    _sitemaps = {}
    for app in applications:
        app_package = import_module(app + ".sitemaps")
        _sitemaps.update(app_package.SITEMAPS)
    return _sitemaps

