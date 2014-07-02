from models.bagni import Bagno
from models.places import Neighbourhood
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
        ret = []
        for _service in Service.objects.prefetch_related("bagni__neighbourhood"):
            for _neighbourhood in _service.bagni.distinct("neighbourhood").values_list("neighbourhood__slug"):
                ret.append((_neighbourhood[0], _service.slug))
        return ret

    def location(self, obj):
        return reverse("bagni-by-facility-and-neighbourhood",
                kwargs={'facility_slug' : obj[1],
                        'neighbourhood_slug' : obj[0],
                        })

SITEMAPS = {
    'bagni' : BagnoSitemap,
    'bagni-static': BagnoStatic,
    'neighbourhood-services': NeighbourhoodFacilitySitemap,
}

