from django.core.cache import cache

from models.bagni import Bagno
from models.services import Service

from ombrelloni.common.sitemaps import LocalesSitemap, StaticLocalesSitemap

from django.core.urlresolvers import reverse

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
        ret = cache.get('sitemap_neighbourhood_facilities_items')
        if ret:
            return ret
        ret = set()
        bagni = Bagno.objects.prefetch_related("neighbourhood", "services")
        for bagno in bagni:
            for service in bagno.services.all():
                ret.add((service.slug, bagno.neighbourhood.slug))
        ret = list(ret) 
        cache.set('sitemap_neighbourhood_facilities_items', ret, 60 * 60 * 24)
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

