# -*- coding: utf-8 -*-
import autoslug

from django.contrib.gis.db import models
from django.db import models as django_models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

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
        cities = self.index_cities(field="name").split("#")
        services = self.index_services(field="name").split("#")
        elems.extend(cities)
        elems.extend(services)
        return unicode(" ".join(elems))

    def index_services(self, field='slug', sep="#"):
        """ Returns a string representing all the bagno services separated by
            the sep val.
            Needed to index the services as listid in whoosh and have facets
        """
        return unicode(sep.join([getattr(s, field) for s in self.services.all()]))


    def index_languages(self, field='slug', sep="#"):
        """ Returns a string representing all the bagno spoken languages separated by
            the sep val.
            Needed to index the languages as listid in whoosh and have facets
        """
        return unicode(sep.join([getattr(l, field) for l in self.languages.all()]))

    def index_cities(self, sep="#", field="slug"):
        cities = []
        if self.neighbourhood:
            cities.append(getattr(self.neighbourhood, field))
            if self.neighbourhood.municipality:
                cities.append(getattr(self.neighbourhood.municipality, field))
                if self.neighbourhood.municipality.district:
                    cities.append(getattr(self.neighbourhood.municipality.district, field))
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

    @models.permalink
    def get_edit_url(self):
        return ("bagno-edit", [self.slug, ])

    @models.permalink
    def get_contactform_url(self):
        return ("bagno-contacts", [self.slug, ])

    def is_managed(self):
        return len(self.managers.all()) > 0

    def can_be_managed_by(self, user):
        is_staff = user.is_staff
        try:
            manager = user.manager
            can_edit = manager.can_edit(self)
        except (ObjectDoesNotExist, AttributeError):
            can_edit = False
        return is_staff or can_edit
