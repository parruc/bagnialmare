# -*- coding: utf-8 -*-
import autoslug

from django.contrib.gis.db import models
from django.db import models as django_models
from django.utils.translation import ugettext_lazy as _


class Bagno(models.Model):
    """ The model for Bagno object
    """
    class Meta:
        verbose_name = _('Bagno')
        verbose_name_plural = _('Bagni')
        app_label = 'bagni'

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
    neighbourhood = models.ForeignKey("Neighbourhood", null=True, related_name='bagni', verbose_name=_("Neighbourhood"), on_delete=django_models.SET_NULL)
    mail = models.EmailField(max_length=50, blank=True)
    site = models.URLField(max_length=75, blank=True)
    point = models.PointField(null=True, blank=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

    def index_text(self):
        """ Text indexed for fulltext search (the what field)
        """
        elems = [self.name, ]
        cities = self.index_cities().split("#")
        services = self.index_services().split("#")
        elems.extend(cities)
        elems.extend(services)
        return unicode(" ".join(elems))

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

    def index_cities(self, sep="#"):
        cities = []
        if self.neighbourhood:
            cities.append(self.neighbourhood.name)
            if self.neighbourhood.municipality:
                cities.append(self.neighbourhood.municipality.name)
                if self.neighbourhood.municipality.district:
                    cities.append(self.neighbourhood.municipality.district.name)
        return unicode(sep.join(cities))

    def index_features(self):
        """ Returns a dictionary representing the whoosh entry for
            the current object in the index
        """
        return dict(id=unicode(self.id),
                    text=self.index_text(),
                    services=self.index_services(),
                    languages=self.index_languages(),
                    )

    @models.permalink
    def get_absolute_url(self):
        return ("bagno", [self.slug, ])

    def get_edit_url(self):
        return ("bagno-edit", [self.slug, ])
