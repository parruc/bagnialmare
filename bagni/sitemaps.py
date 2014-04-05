from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.utils.translation import activate
from models import *

class EnBagnoSitemap(Sitemap):
    def items(self):
        return Bagno.objects.all()

    def location(self, item):
        activate("en")
        return item.get_absolute_url()

class ItBagnoSitemap(Sitemap):
    def items(self):
        return Bagno.objects.all()

    def location(self, item):
        activate("it")
        return item.get_absolute_url()

SITEMAPS = {
    'bagno_en' : EnBagnoSitemap,
    'bagno_it' : ItBagnoSitemap,
}

