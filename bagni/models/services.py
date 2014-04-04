# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail import ImageField
import autoslug

class ServiceCategory(models.Model):
    """ List of categories available for the service
    """
    class Meta:
        verbose_name = _('Service Category')
        verbose_name_plural = _('Service Category')
        app_label = 'bagni'

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
    order = models.IntegerField()
    image = ImageField(upload_to="images/servicecategories", verbose_name=_("Image"), blank=True, null=True )
    slug = autoslug.AutoSlugField(max_length=50,
                                  populate_from='name',
                                  verbose_name=_("Slug"),
                                  unique=True,
                                  editable=True,)
    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ("service-category", [self.slug, ])


class Service(models.Model):
    """ The model for Service object
    """
    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
        app_label = 'bagni'

    name = models.CharField(max_length=50)
    description = models.TextField(max_length=2000, blank=True)
    slug = autoslug.AutoSlugField(max_length=50,
                                  populate_from='name',
                                  verbose_name=_("Slug"),
                                  unique=True,
                                  editable=True,)
    # TODO: A regime mettere  obbligatorio cateogry
    category = models.ForeignKey(ServiceCategory, blank=True, null=True, related_name='services', verbose_name=_("Category"),)
    image = ImageField(upload_to="images/services", verbose_name=_("Image"), blank=True, null=True)
    free = models.BooleanField(default=True,)

    @models.permalink
    def get_absolute_url(self):
        return ("service", [self.slug, ])

    def get_filtered_search_url(self):
        """ The search url to activate this (and only this) facet as filter
        """
        return reverse("search") + "?f=services:" + self.name + "@" + self.category.name

    def __unicode__(self):
        return self.name
