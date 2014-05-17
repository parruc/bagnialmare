from models.bagni import Bagno
from models.services import Service

from ombrelloni.common.sitemaps import LocalesSitemap, StaticLocalesSitemap

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

