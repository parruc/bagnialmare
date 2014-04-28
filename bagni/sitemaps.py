from models.bagni import Bagno
from models.services import Service

from common import LocalesSitemap, StaticLocalesSitemap

class BagnoSitemap(LocalesSitemap):
    def items(self):
        return Bagno.objects.all()

class ServiceSitemap(LocalesSitemap):
    def items(self):
        return Service.objects.all()

class BagnoStatic(StaticLocalesSitemap):
    def items(self):
        return ['homepage', 'about-us', 'services', 'neighbourhoods', 'municipalities', 'districts']

SITEMAPS = {
    'bagni' : BagnoSitemap,
    'services' : ServiceSitemap,
    'bagni-static': BagnoStatic,
}

