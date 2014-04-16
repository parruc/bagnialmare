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
    option_list = BaseCommand.option_list + (
        make_option("-l", "--limit",
                    action="store", type="int",
                    dest="limit"),
        make_option("-s", "--startfrom",
                    action="store", type="int",
                    dest="startfrom"),
    )

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
                if name in ["Alcide Spiaggia", "Alberto"]:
                    name = "Bagno " + name
                b = Bagno.objects.filter(name=name)
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
                        t = Telephone(name=name)
                        t.number = number.strip()
                        t.bagno = b
                        t.save()

                        logger.warning("Bagno [%d/%d]assigning telephone %s: %s  to bagno %s" % (count, tot, t.name, t.number, b.name, ) )


