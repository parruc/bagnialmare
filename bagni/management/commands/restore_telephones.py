from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point
from django.utils.translation import ugettext_lazy as _
from bagni.models import Bagno, Telephone
from optparse import make_option
import json
import re
import logging

logging.basicConfig()
logger = logging.getLogger("bagni.console")
#logger.setLevel(logging.WARNING)

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--startfrom', '-s', type=int)
        parser.add_argument('--limit', '-l', type=int)


    def handle(self, *args, **options):
        logger.info("Restoring Telephone numbers")
        Telephone.objects.all().delete()
        bagni = []
        cities = ["cervia", "cesenatico", "ferrara", "ravenna", "rimini", "riccione", "bellaria-igea-marina"]
        for city in cities:
            try:
                with open('scripts/scraping/output_' + city + '.json', 'r') as output_file:
                    bagni += json.load(output_file)
            except IOError:
                raise CommandError("cannot open 'scripts/scraping/output_" + city + ".json' Have you generated it?")

        tel_names = {'tel': _("Telephone number"), 'cell': _("Mobile number"), 'winter_tel': _("Winter number"), 'fax': _("Fax number")}
        tot = len(bagni)
        for count, bagno in enumerate(bagni):
            point = Point([float(coord) for coord in reversed(bagno['coords'])])
            try:
                name = bagno['name'].replace("- 82 ", "")
                names = [name, "Bagno " + name]
                b = Bagno.objects.filter(name__in=names)
                if len(b) == 1:
                    b = b[0]
                else:
                    b = b.get(point=point)
            except:
                import ipdb; ipdb.set_trace()

            if not b:
                import ipdb; ipdb.set_trace()
            for field in ["tel", "cell", "winter_tel", "fax"]:
                if field in bagno:
                    numeri = re.split("-\n", bagno[field])
                    for index,number in enumerate(numeri):
                        name = tel_names[field]
                        if len(numeri) > 1:
                            name += " " + str(index+1)
                        t = Telephone(name=name, number=number.strip(), bagno=b)
                        try:
                            t.save()
                        except:
                            numbers_post = {"Davide": "335 5851390", "Bagno 96": "0541 377260", "Guido": "0541 377260", "Bagno 97": "0541 377236", "Oriano": "339 3910410"}
                            for name, number in numbers_post.items():
                                t=Telephone(name=name, number=number, bagno=b)
                                t.save()

                        logger.warning("Bagno [%d/%d]assigning telephone %s: %s  to bagno %s" % (count, tot, t.name, t.number, b.name, ) )


