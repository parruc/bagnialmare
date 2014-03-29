# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _

import autoslug


class District(models.Model):
    """The model for the District object
    """
    class Meta:
        verbose_name = _('District')
        verbose_name_plural = _('Districts')
        app_label = 'bagni'

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=2000, blank=True)
    slug = autoslug.AutoSlugField(max_length=50,
                                  populate_from='name',
                                  verbose_name=_("Slug"),
                                  unique=True,
                                  editable=True,)
    @models.permalink
    def get_absolute_url(self):
        return ("district", [self.slug, ])

    def __unicode__(self):
        return self.name


class Municipality(models.Model):
    """The model for the Municipality object
    """

    class Meta:
        verbose_name = _('Municipality')
        verbose_name_plural = _('Municipalities')
        app_label = 'bagni'

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=2000, blank=True)
    district = models.ForeignKey(District, related_name="municipalities", verbose_name=_("District"),)
    slug = autoslug.AutoSlugField(max_length=50,
                                  populate_from='name',
                                  verbose_name=_("Slug"),
                                  unique=True,
                                  editable=True,)
    @models.permalink
    def get_absolute_url(self):
        return ("municipality", [self.slug, ])

    def __unicode__(self):
        return self.name


class Neighbourhood(models.Model):
    """The model for the Neighbourhood object
    """
    class Meta:
        verbose_name = _('Neighbourhood')
        verbose_name_plural = _('Neighbourhoods')
        app_label = 'bagni'

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=2000, blank=True)
    municipality = models.ForeignKey(Municipality, related_name='neighbourhoods', verbose_name=_("Municipality"), )
    slug = autoslug.AutoSlugField(max_length=50,
                                  populate_from='name',
                                  verbose_name=_("Slug"),
                                  unique=True,
                                  editable=True,)
    @models.permalink
    def get_absolute_url(self):
        return ("neighbourhood", [self.slug, ])

    def __unicode__(self):
        return self.name
