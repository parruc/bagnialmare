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
#logger.setLevel(logging.WARNING)

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("-l", "--limit",
                    action="store", type="int",
                    dest="limit"),
        make_option("-s", "--startfrom",
                    action="store", type="int",
                    dest="startfrom"),
    )

    def handle(self, *args, **options):
        logger.info("Restoring Neighbourhood Municipalities Districts")
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
        if 'limit' in options and options['limit'] < len(bagni):
            bagni = bagni[:options['limit']]
        if 'startfrom' in options and options['startfrom'] < len(bagni):
            bagni = bagni[options['startfrom']:]
        tot = len(bagni)
        for count, bagno in enumerate(bagni):
            n = m = d = None
            n_name = m_name = d_name = None
            text_point = ",".join(bagno['coords'])
            point = Point([float(coord) for coord in reversed(bagno['coords'])])
            try:
                name = bagno['name'].replace("- 82 ", "")
                if name in ["Alcide Spiaggia", "Alberto"]:
                    name = "Bagno " + name
                b = Bagno.objects.filter(name=name)
                if len(b) == 1:
                    b = b[0]
                else:
                    b = b.get(point=point)
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

                for address_part in result['results'][0]['address_components']:
                    if "locality" in address_part['types']:
                        json_neighbourhood = bagno.get("neighbourhood", None)
                        if json_neighbourhood and json_neighbourhood != address_part["long_name"]:
                            n_name = json_neighbourhood
                        else:
                            n_name = address_part["long_name"]
                    elif "administrative_area_level_3" in address_part['types']:
                        m_name = address_part["long_name"]
                    elif "administrative_area_level_2" in address_part['types']:
                        d_name = address_part["long_name"]
                if not (n_name and m_name and d_name):
                    if not n_name:
                        if "neighbourhood" in bagno and bagno["neighbourhood"]:
                            n_name = bagno['neighbourhood']
                        elif bagno['address'] == "Fontanelle Abissinia":
                            n_name = "Riccione"
                        else:
                            import ipdb; ipdb.set_trace()
                    elif n_name == "Torre Pedrera":
                        m_name = d_name = "Rimini"
                    else:
                        import ipdb; ipdb.set_trace()
                if bagno['address'] == "Via Spazzoli Tonino, 3":
                    b.address = "Via Giovanni Spallazzi, 1"
                    b.save()
                if n_name == "Casalborsetti":
                    n_name = "Casal Borsetti"
                cache[h] = (n_name, m_name, d_name)
                with open("restore_cities.json", 'w') as outfile:
                    json.dump(cache, outfile)
            d = District.objects.filter(name=d_name)
            if not d:
                logger.info("creating district %s" % d_name)
                d = District(name=d_name)
                d.save()
            else:
                d = d[0]
            m = Municipality.objects.filter(name=m_name)
            if not m:
                logger.info("creating municipality %s" % m_name)
                m = Municipality(name=m_name)
                m.district = d
                m.save()
            else:
                m = m[0]

            n = Neighbourhood.objects.filter(name=n_name)
            if not n:
                logger.info("creating neighbourhood %s" % n_name)
                n = Neighbourhood(name=n_name)
                n.municipality = m
                n.save()
            else:
                n = n[0]
            b.neighbourhood = n
            logger.info("[%d/%d]assigning neighbourhood %s municipality %s city %s to bagno %s" % (count, tot, n.name, m.name, d.name, b.name, ) )
            b.save()
