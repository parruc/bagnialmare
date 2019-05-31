# -*- coding: utf-8 -*-
from datetime import date

from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _


class Booking(models.Model):

    bagno = models.ForeignKey("bagni.Bagno", related_name='bookings',
                              verbose_name=_("Bagno"), on_delete=models.CASCADE)
    start = models.DateField(verbose_name=_("From"),
                             default=date.today)
    end = models.DateField(verbose_name=_("To"),
                           default=date.today)
    sunbeds = models.IntegerField(verbose_name=_("Number of subnbeds"),
                                  default=2)
    umbrellas = models.IntegerField(verbose_name=_("Number of umbrellas"),
                                    default=1)
    email = models.EmailField(max_length=100,
                              verbose_name=_("Email"),)
    mobile = models.CharField(max_length=100,
                              verbose_name=_("Mobile"),)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
