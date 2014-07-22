# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail import ImageField
from ckeditor.fields import RichTextField

from . import BaseModel


class ServiceCategory(BaseModel):
    """ List of categories available for the service
    """
    class Meta:
        verbose_name = _('Service Category')
        verbose_name_plural = _('Service Category')
        app_label = 'bagni'

    description = RichTextField(blank=True, max_length=2000, verbose_name=_("Description"),)
    order = models.IntegerField()
    image = ImageField(upload_to="images/servicecategories", verbose_name=_("Image"), blank=True, null=True )

    @models.permalink
    def get_absolute_url(self):
        return ("service-category", [self.slug, ])


class Service(BaseModel):
    """ The model for Service object
    """
    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
        app_label = 'bagni'

    description = RichTextField(blank=True, max_length=2000, verbose_name=_("Description"),)

    # TODO: A regime mettere  obbligatorio cateogry
    seo_name =  models.CharField(max_length=100, blank=True, null=True,)
    aliases = models.CharField(max_length=300, blank=True, null=True,)
    category = models.ForeignKey(ServiceCategory, blank=True, null=True, related_name='services', verbose_name=_("Category"),)
    image = ImageField(upload_to="images/services", verbose_name=_("Image"), blank=True, null=True)
    free = models.BooleanField(default=True,)

    @models.permalink
    def get_absolute_url(self):
        return ("service", [self.slug, ])

    def get_filtered_search_url(self):
        """ The search url to activate this (and only this) facet as filter
        """
        return reverse("search") + "?f=services:" + self.slug
