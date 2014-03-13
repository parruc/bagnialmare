from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point
from bagni.models import Bagno, Service, Municipality, District, Language
from optparse import make_option
import simplejson
import logging

logging.basicConfig()
logger = logging.getLogger("bagni.console")

class Command(BaseCommand):
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        logger.info("loading bagni objects from json files")
        bagni = {}
        name_clashes = 0
        missing_neighbourhoods = 0
        missing_municipality = 0
        missing_municipality_and_neighbourhood = 0
        found_missing = 0
        not_enough = 0
        cities = ["cervia", "cesenatico", "ferrara", "ravenna", "rimini", "riccione", "bellaria-igea-marina"]
        for city in cities:
            logger.info("loading city: %s" % (city,))
            with open('scripts/scraping/output_' + city + '.json', 'r') as json_file:
                loaded_bagni = simplejson.load(json_file)
            for bagno in loaded_bagni:
                if bagni.has_key(bagno["name"]):
                    name_clashes += 1
                    logger.warning("name clash: %s" % (bagno["name"],))
                if not bagno.has_key("neighbourhood"):
                    missing_neighbourhoods += 1
                    logger.warning("missing neighbourhood: %s" % (bagno["name"]))
                if not bagno.has_key("municipality"):
                    missing_municipality += 1
                    logger.warning("missing municipality: %s" % (bagno["name"]))
                if not bagno.has_key("neighbourhood") and not bagno.has_key("municipality"):
                    missing_municipality_and_neighbourhood += 1
                    db_bagni = Bagno.objects.filter(name__iexact=bagno["name"], address__iexact=bagno["address"])
                    if len(db_bagni) == 1:
                        found_missing += 1
                    elif len(db_bagni) > 1:
                        not_enough += 1
                bagni[bagno["name"]] = bagno
        logger.info("total missing neighbourhood: %d" % (missing_neighbourhoods,))
        logger.info("total missing municipality: %d" % (missing_municipality,))
        logger.info("total missing municipality and neighbourhood: %d" % (missing_municipality_and_neighbourhood,))
        logger.info("matched missing in db: %d" % (found_missing,))
        logger.info("unmatched missing in db: %d" % (not_enough,))
        logger.info("total name clashes: %d" % (name_clashes,))
