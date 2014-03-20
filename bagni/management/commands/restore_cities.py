from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point
from bagni.models import Bagno, Neighbourhood, Municipality, District
from optparse import make_option
import requests
import json
import logging
<<<<<<< HEAD
import hashlib

logging.basicConfig()
logger = logging.getLogger("bagni.console")
logger.setLevel(logging.WARNING)
=======

logging.basicConfig()
logger = logging.getLogger("bagni.console")
>>>>>>> a56eefc0fb1a9f782b96cc6e8bad8c66acfac3fc

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("-l", "--limit",
                    action="store", type="int",
                    dest="limit"),
        )

    def handle(self, *args, **options):
<<<<<<< HEAD
        logger.warning("Restoring Neighbourhood Municipalities Districts")
        Municipality.objects.all().delete()
        District.objects.all().delete()
        Neighbourhood.objects.all().delete()
=======
        logger.info("Restoring Municipalities and Districts")
        Municipality.objects.all().delete()
        District.objects.all().delete()
>>>>>>> a56eefc0fb1a9f782b96cc6e8bad8c66acfac3fc
        bagni = []
        cities = ["cervia", "cesenatico", "ferrara", "ravenna", "rimini", "riccione", "bellaria-igea-marina"]
        for city in cities:
            try:
                with open('scripts/scraping/output_' + city + '.json', 'r') as output_file:
                    bagni += json.load(output_file)
            except IOError:
                raise CommandError("cannot open 'scripts/scraping/output_" + city + ".json' Have you generated it?")
<<<<<<< HEAD
        with open("restore_cities.json", 'r') as outfile:
            cache = json.load(outfile)
        base_url = "https://maps.googleapis.com/maps/api/geocode/json?latlng={}&sensor=true"
=======

>>>>>>> a56eefc0fb1a9f782b96cc6e8bad8c66acfac3fc
        if 'limit' in options and options['limit'] > len(bagni):
            bagni = bagni[:options['limit']]
        for bagno in bagni:
            n = m = d = None
            text_point = ",".join(bagno['coords'])
<<<<<<< HEAD
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
=======
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
>>>>>>> a56eefc0fb1a9f782b96cc6e8bad8c66acfac3fc
                m.district = d
                m.save()
            else:
                m = m[0]

<<<<<<< HEAD
            n = Neighbourhood.objects.filter(name=n_name)
            if not n:
                logger.warning("creating neighbourhood %s" % n_name)
                n = Neighbourhood(name=n_name)
=======
            n = Neighbourhood.objects.filter(name=politicals[0])
            if not n:
                logger.info("creating neighbourhood %s" % politicals[0])
                n = Neighbourhood(name=politicals[0])
>>>>>>> a56eefc0fb1a9f782b96cc6e8bad8c66acfac3fc
                n.municipality = m
                n.save()
            else:
                n = n[0]
            b.neighbourhood = n
<<<<<<< HEAD
            logger.warning("assigning neighbourhood %s municipality %s city %s to bagno %s" % (n.name, m.name, d.name, b.name, ) )
            b.save()
=======
            b.save()

>>>>>>> a56eefc0fb1a9f782b96cc6e8bad8c66acfac3fc
