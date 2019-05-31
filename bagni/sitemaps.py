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

class NeighbourhoodFacilitySitemap(LocalesSitemap):
    def items(self):
        lang = get_language()
        ret = cache.get('sitemap_neighbourhood_facilities_items_' + lang)
        if ret:
            return ret
        ret = set()
        bagni = Bagno.objects.prefetch_related("neighbourhood", "services")
        for bagno in bagni:
            for service in bagno.services.all():
                ret.add((service.slug, bagno.neighbourhood.slug))
        ret = list(ret)
        cache.set('sitemap_neighbourhood_facilities_items_' + lang, ret, 60 * 60 * 24)
        return ret

    def location(self, obj):
        return reverse("bagni-by-facility-and-neighbourhood",
                kwargs={'facility_slug' : obj[0],
                        'neighbourhood_slug' : obj[1],
                        })

SITEMAPS = {
    'bagni' : BagnoSitemap,
    'bagni-static': BagnoStatic,
    'neighbourhood-services': NeighbourhoodFacilitySitemap,
}

