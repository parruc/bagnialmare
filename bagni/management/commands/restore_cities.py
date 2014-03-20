from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point
from bagni.models import Bagno, Neighbourhood, Municipality, District
from optparse import make_option
import requests
import json
import logging
import hashlib

logging.basicConfig()
logger = logging.getLogger("bagni.console")
logger.setLevel(logging.WARNING)

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("-l", "--limit",
                    action="store", type="int",
                    dest="limit"),
        )

    def handle(self, *args, **options):
        logger.warning("Restoring Neighbourhood Municipalities Districts")
        Municipality.objects.all().delete()
        District.objects.all().delete()
        Neighbourhood.objects.all().delete()
        bagni = []
        cities = ["cervia", "cesenatico", "ferrara", "ravenna", "rimini", "riccione", "bellaria-igea-marina"]
        for city in cities:
            try:
                with open('scripts/scraping/output_' + city + '.json', 'r') as output_file:
                    bagni += json.load(output_file)
            except IOError:
                raise CommandError("cannot open 'scripts/scraping/output_" + city + ".json' Have you generated it?")
        with open("restore_cities.json", 'r') as outfile:
            cache = json.load(outfile)
        base_url = "https://maps.googleapis.com/maps/api/geocode/json?latlng={}&sensor=true"
        if 'limit' in options and options['limit'] > len(bagni):
            bagni = bagni[:options['limit']]
        for bagno in bagni:
            n = m = d = None
            text_point = ",".join(bagno['coords'])
            point = Point([float(coord) for coord in reversed(bagno['coords'])])
            try:
                name = bagno['name'].strip("- 82 ")
                b = Bagno.objects.get(name=name, point=point)
            except:
                import ipdb; ipdb.set_trace()
            h = hashlib.sha224(bagno['name'].encode('ascii', errors='ignore') + text_point).hexdigest()
            if h in cache:
                (n_name, m_name, d_name) = cache[h]
            else:
                url = base_url.format(text_point)
                try:
                    r = requests.get(url)
                    result = json.loads(r.content)

                    if not b:
                        import ipdb; ipdb.set_trace()
                        pass
                except Exception as ex:
                    import ipdb; ipdb.set_trace()
                    ex
                    pass

                politicals = []
                for address_part in result['results'][0]['address_components']:
                    if "political" in address_part['types']:
                        politicals.append(address_part["long_name"])
                if len(politicals) < 3:
                    import ipdb; ipdb.set_trace()
                    pass
                d_name = politicals[2]
                m_name = politicals[1]
                n_name = politicals[0]
                cache[h] = (n_name, m_name, d_name)
                with open("restore_cities.json", 'w') as outfile:
                    json.dump(cache, outfile)

            d = District.objects.filter(name=d_name)
            if not d:
                logger.warning("creating district %s" % d_name)
                d = District(name=d_name)
                d.save()
            else:
                d = d[0]
            m = Municipality.objects.filter(name=m_name)
            if not m:
                logger.warning("creating municipality %s" % m_name)
                m = Municipality(name=m_name)
                m.district = d
                m.save()
            else:
                m = m[0]

            n = Neighbourhood.objects.filter(name=n_name)
            if not n:
                logger.warning("creating neighbourhood %s" % n_name)
                n = Neighbourhood(name=n_name)
                n.municipality = m
                n.save()
            else:
                n = n[0]
            b.neighbourhood = n
            logger.warning("assigning neighbourhood %s municipality %s city %s to bagno %s" % (n.name, m.name, d.name, b.name, ) )
            b.save()
