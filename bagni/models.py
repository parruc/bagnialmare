# -*- coding: utf-8 -*-
import time
import random
import os

from django.core.urlresolvers import reverse
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail import ImageField
import autoslug



class District(models.Model):
    """The model for the District object
    """
    class Meta:
        verbose_name = _('District')
        verbose_name_plural = _('Districts')

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


class Language(models.Model):
    """ List of languages available for the spoken language field in bagno
    """
    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
    slug = autoslug.AutoSlugField(max_length=50,
                                  populate_from='name',
                                  verbose_name=_("Slug"),
                                  unique=True,
                                  editable=True,)
    def __unicode__(self):
        return self.name


class ServiceCategory(models.Model):
    """ List of categories available for the service
    """
    class Meta:
        verbose_name = _('Service Category')
        verbose_name_plural = _('Service Category')

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
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


class Bagno(models.Model):
    """ The model for Bagno object
    """
    class Meta:
        verbose_name = _('Bagno')
        verbose_name_plural = _('Bagni')

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
    slug = autoslug.AutoSlugField(max_length=50,
                                  populate_from='name',
                                  verbose_name=_("Slug"),
                                  unique=True,
                                  editable=True,)
    number = models.CharField(max_length=30, blank=True)
    languages = models.ManyToManyField("Language", blank=True, related_name='bagni')
    services = models.ManyToManyField("Service", blank=True, related_name='bagni')
    address = models.CharField(max_length=100, blank=True)
    # TODO: A regime mettere  obbligatorio municipality
    municipality = models.ForeignKey(Municipality, blank=True, null=True, related_name='bagni', verbose_name=_("Municipality"), )
    mail = models.EmailField(max_length=50, blank=True)
    site = models.URLField(max_length=75, blank=True)
    point = models.PointField(null=True, blank=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

    def index_text(self):
        """ Text indexed for fulltext search (the what field)
        """
        municipality_name = district_name = ""
        if self.municipality:
            municipality_name = self.municipality.name
            if self.municipality.district:
                district_name = self.municipality.district.name
        elems = (self.name, self.index_services(), municipality_name, district_name)
        return unicode("%s %s %s %s" % elems)

    def index_services(self, sep="#"):
        """ Returns a string representing all the bagno services separated by
            the sep val.
            Needed to index the services as listid in whoosh and have facets
        """
        return unicode(sep.join([s.name+"@"+s.category.name for s in self.services.all()]))


    def index_languages(self, sep="#"):
        """ Returns a string representing all the bagno spoken languages separated by
            the sep val.
            Needed to index the languages as listid in whoosh and have facets
        """
        return unicode(sep.join([l.name for l in self.languages.all()]))

    def index_features(self):
        """ Returns a dictionary representing the whoosh entry for
            the current object in the index
        """
        return dict(id=unicode(self.id),
                    text=self.index_text(),
                    services=unicode(self.index_services()),
                    languages=unicode(self.index_languages()),
                    )

    @models.permalink
    def get_absolute_url(self):
        return ("bagno", [self.slug, ])

    def get_edit_url(self):
        return ("bagno-edit", [self.slug, ])


class Telephone(models.Model):
    """ List of telephone numbers of the bagno
    """
    class Meta:
        verbose_name = _('Telephone number')
        verbose_name_plural = _('Telephone numbers')

    name = models.CharField(max_length=25)
    number = models.CharField(max_length=100)
    bagno = models.ForeignKey(Bagno, related_name="telephones", verbose_name=_("Bagno"),)
    def __unicode__(self):
        return self.name


class Service(models.Model):
    """ The model for Service object
    """
    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')

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
        return reverse("search") + "?f=services:" + self.name

    def __unicode__(self):
        return self.name


class Image(models.Model):
    """ Model used for the bagno images
        TODO: inline in admin form of bagno?
    """
    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')

    def _define_filename(self, filename):
        upload_base_path = "images/bagni"
        upload_path = "%s/%s/%s" % (upload_base_path,
                                    self.bagno.slug,
                                    filename)
        return upload_path


    name = models.CharField(max_length=50)
    description = models.TextField(max_length=2000, blank=True)
    slug = autoslug.AutoSlugField(max_length=50,
                                  populate_from='name',
                                  verbose_name=_("Slug"),
                                  unique=True,
                                  editable=True,)
    image = ImageField(upload_to=_define_filename, verbose_name=_("Image"),)
    bagno = models.ForeignKey(Bagno, related_name="images", verbose_name=_("Bagno"),)
