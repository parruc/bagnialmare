# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from bagni.models import Service
import logging

logging.basicConfig()
logger = logging.getLogger("bagni.console")

TO_HIDE = ["accettazione bancomat", "alcohol tester", "area verde", "cabine",
           "carte di credito", "cene a tema", "concerti live",
           "corsi di beach volley", "corsi di racchettoni", "custodia valori",
           "deposito caschi", "kick boxing", "mosconi", "passeggini",
           "piano bar", "ping pong", "pizzeria", "rimessaggio barche",
           "scolaresche", "sea volley", "serate degustazione", "spazio tv",
           "spiaggine", "tornei sportivi", "videogiochi", "beach soccer",
           "calcio balilla", "frigoriferi", "campo da tennis",
           "trampolino elastico", "libreria", "sparring vlup", "docce calde",
           "ginnastica", "idromassaggio", "bookcrossing", "giochi di società",
           "canotti e materassini", "area picnic", "dancing", ]

REPLACE_DICT = {
    "animazione preserale": "animazione",
    "animazione serale": "animazione",
    "beach basket": "basket",
    "giochi da tavolo": "giochi di società",
    "grigliate di carne": "area barbecue",
    "grigliate di pesce": "area barbecue",
    "internet": "wi-fi",
    "juke box": "musica",
    "parco giochi": "baby park",
    "tavolo da gioco": "giochi di società",
    "terrazza prendisole": "solarium",
    "tornei da tavolo": "giochi di società",
    "trattamenti estetici": "area benessere",
    "windsurf": "surf",
    "cabina surf e windsurf": "surf",
    "paninoteca": "bar",
    "corsi di tennis": "campo da tennis",
    "spinning": "area fitness",
    "feste danzanti": "dancing",
    "massaggi": "area benessere",
    "palestra": "area fitness",
    "area verde": "area picnic"
}

"""
To rename after: 
area barbecue -> barbecue
area benessere -> area massaggi e benessere
surf -> surf e windsurf
"""

class Command(BaseCommand):

    def handle(self, *args, **options):
	    option_list = BaseCommand.option_list
	    for to_hide in TO_HIDE:
		try:
			service_to_hide = Service.objects.get(name_it__iexact=to_hide)	
		except:
			import ipdb; ipdb.set_trace()
		service_to_hide.hidden = True
		service_to_hide.save()
	    for old, new in REPLACE_DICT.items():
		try:
			old_service = Service.objects.get(name_it__iexact=old)
			new_service = Service.objects.get(name_it__iexact=new)
			for bagno in old_service.bagni.all():
			    bagno.services.remove(old_service)
			    bagno.services.add(new_service)
			    bagno.save()
			old_service.delete()
		except:
			import ipdb; ipdb.set_trace()

