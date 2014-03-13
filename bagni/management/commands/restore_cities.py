from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point
from bagni.models import Bagno, Neighbourhood, Municipality, District
from optparse import make_option
import requests
import json
import logging

logging.basicConfig()
logger = logging.getLogger("bagni.console")

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("-l", "--limit",
                    action="store", type="int",
                    dest="limit"),
        )

    def handle(self, *args, **options):
        logger.info("Restoring Municipalities and Districts")
        Municipality.objects.all().delete()
        District.objects.all().delete()
        bagni = []
        cities = ["cervia", "cesenatico", "ferrara", "ravenna", "rimini", "riccione", "bellaria-igea-marina"]
        for city in cities:
            try:
                with open('scripts/scraping/output_' + city + '.json', 'r') as output_file:
                    bagni += json.load(output_file)
            except IOError:
                raise CommandError("cannot open 'scripts/scraping/output_" + city + ".json' Have you generated it?")

        if 'limit' in options and options['limit'] > len(bagni):
            bagni = bagni[:options['limit']]
        for bagno in bagni:
            n = m = d = None
            text_point = ",".join(bagno['coords'])
            base_url = "https://maps.googleapis.com/maps/api/geocode/json?latlng={}&sensor=true"
            url = base_url.format(text_point)
            try:
                r = requests.get(url)
                result = json.loads(r.content)
                point = Point([float(coord) for coord in reversed(bagno['coords'])])
                b = Bagno.objects.filter(point__distance_lte=(point, 5))[0]
                if len(b) != 1:
                    import ipdb; ipdb.set_trace()
            except Exception as ex:
                import ipdb; ipdb.set_trace()
                pass

            politicals = []
            for address_part in result['results'][0]['address_components']:
                if "political" in address_part['types']:
                    politicals.append(address_part["long_name"])
            if len(politicals) < 3:
                import ipdb; ipdb.set_trace()

            d = District.objects.filter(name=politicals[2])
            if not d:
                logger.info("creating district %s" % politicals[2])
                d = District(name=politicals[2])
                d.save()
            else:
                d = d[0]
            m = Municipality.objects.filter(name=politicals[1])
            if not m:
                logger.info("creating municipality %s" % politicals[1])
                m = Municipality(name=politicals[1])
                m.district = d
                m.save()
            else:
                m = m[0]

            n = Neighbourhood.objects.filter(name=politicals[0])
            if not n:
                logger.info("creating neighbourhood %s" % politicals[0])
                n = Neighbourhood(name=politicals[0])
                n.municipality = m
                n.save()
            else:
                n = n[0]
            b.neighbourhood = n
            b.save()

