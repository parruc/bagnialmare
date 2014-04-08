from common import *

class ContactStatic(StaticLocalesSitemap):
    def items(self):
        return ['contact-form']

SITEMAPS = {
    'contacts-static': ContactStatic,
}
