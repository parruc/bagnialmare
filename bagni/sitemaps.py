from django.core.cache import cache

from bagni.models.bagni import Bagno
from bagni.models.services import Service

from bagnialmare.common.sitemaps import LocalesSitemap, StaticLocalesSitemap

from django.urls import reverse
from django.utils.translation import get_language

class BagnoSitemap(LocalesSitemap):
    def items(self):
        return Bagno.objects.all()

class ServiceSitemap(LocalesSitemap):
    def items(self):
        return Service.objects.all()

class BagnoStatic(StaticLocalesSitemap):
    def items(self):
        return ['homepage', 'bagni', 'search']


SITEMAPS = {
    'bagni' : BagnoSitemap,
    'bagni-static': BagnoStatic,
}

