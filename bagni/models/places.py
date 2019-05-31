# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

from . import BaseModel


class District(BaseModel):
    """The model for the District object
    """
    class Meta:
        verbose_name = _('District')
        verbose_name_plural = _('Districts')
        app_label = 'bagni'

    description = models.TextField(max_length=2000, blank=True)

    def get_absolute_url(self):
        return reverse("district", [self.slug, ])


class Municipality(BaseModel):
    """The model for the Municipality object
    """

    class Meta:
        verbose_name = _('Municipality')
        verbose_name_plural = _('Municipalities')
        app_label = 'bagni'

    description = models.TextField(max_length=2000, blank=True)
    district = models.ForeignKey(District, related_name="municipalities", verbose_name=_("District"), on_delete=models.CASCADE, )

    def get_absolute_url(self):
        return reverse("municipality", [self.slug, ])


class Neighbourhood(BaseModel):
    """The model for the Neighbourhood object
    """
    class Meta:
        verbose_name = _('Neighbourhood')
        verbose_name_plural = _('Neighbourhoods')
        app_label = 'bagni'

    description = models.TextField(max_length=2000, blank=True)
    municipality = models.ForeignKey(Municipality, related_name='neighbourhoods', verbose_name=_("Municipality"), on_delete=models.CASCADE, )

    def get_absolute_url(self):
        return reverse("neighbourhood", [self.slug, ])
