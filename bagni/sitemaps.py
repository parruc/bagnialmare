from models import *
from common import LocalesSitemap, StaticLocalesSitemap

class BagnoSitemap(LocalesSitemap):
    def items(self):
        return Bagno.objects.all()

class BagnoStatic(StaticLocalesSitemap):
    def items(self):
        return ['homepage', 'about-us', 'services', 'neighbourhoods', 'municipalities', 'districts']

SITEMAPS = {
    'bagni' : BagnoSitemap,
    'bagni-static': BagnoStatic,
}

