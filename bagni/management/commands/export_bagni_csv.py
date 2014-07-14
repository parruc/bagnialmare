from django.core.management.base import BaseCommand, CommandError
from bagni.models import Bagno, Neighbourhood, Municipality
from optparse import make_option
import datetime
import logging

logging.basicConfig()
logger = logging.getLogger("bagni.console")

OUTPUT_PATH = "ombrelloni/fixtures/bagni_%s.csv"
SEPARATOR = u";"
DATEFMT = "%d/%m/%Y %H:%M"

class Command(BaseCommand):
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        counter = 0
        _output_path = OUTPUT_PATH % (datetime.datetime.now().strftime("%d_%m_%Y"),)
        logger.info("export bagni to csv file: %s" % (_output_path,))
        with open(_output_path, "wt") as output:
            for bagno in Bagno.objects.prefetch_related("neighbourhood", "neighbourhood__municipality", "managers").all():
                data = [u"%d" % (bagno.pk,),
                        bagno.name,
                        bagno.number,
                        bagno.mail,
                        bagno.site,
                        bagno.neighbourhood.municipality.name,
                        bagno.neighbourhood.name,
                        bagno.created.strftime(DATEFMT),
                        bagno.managers.first().created.strftime(DATEFMT) if bagno.managers.exists() else "",
                        u"http://bagnialmare.com/admin/bagni/bagno/%s" % (str(bagno.pk),),
                        ]
                counter += 1
                outstring = SEPARATOR.join(data) + SEPARATOR + '\n'
                output.write(outstring.encode('utf8'))
        logger.info("exported %d bagni" % (counter,))
