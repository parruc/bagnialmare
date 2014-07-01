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
        for neighbourhood in Neighbourhood.objects.all():
            for facility in Service.objects.all():
                ret.append((neighbourhood, facility))
        return ret

    def location(self, obj):
        return reverse("bagni-by-facility-and-neighbourhood",
                kwargs={'facility_slug' : obj[1].slug,
                        'neighbourhood_slug' : obj[0].slug,
                        })

SITEMAPS = {
    'bagni' : BagnoSitemap,
    'bagni-static': BagnoStatic,
    'neighbourhood-services': NeighbourhoodFacilitySitemap,
}

