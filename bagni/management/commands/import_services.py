from django.core.management.base import BaseCommand, CommandError
from bagni.models import Service, ServiceCategory
from optparse import make_option
import simplejson
import logging

logger = logging.getLogger("bagni.console")


class Command(BaseCommand):
        def add_arguments(self, parser):
            parser.add_argument('--limit', '-l', type=int)

    def handle(self, *args, **options):
        Service.objects.all().delete()
        ServiceCategory.objects.all().delete()
        services = []
        categories = {}
        aliases = {}

        try:
            with open('scripts/scraping/services.json', 'r') as services_file:
                services += simplejson.load(services_file)
        except IOError:
            raise CommandError("cannot open 'scripts/scraping/services.json' Have you generated it?")

        try:
            with open('scripts/scraping/services_categories.json', 'r') as categories_file:
                categories.update(simplejson.load(categories_file))
        except IOError:
            raise CommandError("cannot open 'scripts/scraping/services_categories.json'. Try to git pull")

        try:
            with open('scripts/scraping/services_aliases.json', 'r') as aliases_file:
                aliases.update(simplejson.load(aliases_file))
        except IOError:
            raise CommandError("cannot open 'scripts/scraping/services_aliases.json'. Try to git pull")

        if 'limit' in options and options['limit'] > len(services):
            services = services[:options['limit']]
        for service in services:
            try:
                s = Service(name=service)
                if service in aliases:
                    service = aliases[service]
                if service in categories:
                    category = categories.get(service, '')
                    c = ServiceCategory.objects.filter(name=category)
                    if not c:
                        c = ServiceCategory(name=category)
                        c.save()
                    else:
                        c = c[0]
                    s.category = c
                else:
                    logger.warning("Service %s does not fit any category" % (service, ))
                s.save()
            except Exception as e:
                logger.error("Importazione del servizio %s fallita con errore %s", (service, e))
