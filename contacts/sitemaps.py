from ombrelloni.common.sitemaps import StaticLocalesSitemap

class ContactStatic(StaticLocalesSitemap):
    def items(self):
        return ['contact-form']

SITEMAPS = {
    'contacts-static': ContactStatic,
}

