from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MaxLengthValidator
from ckeditor.fields import RichTextField
from django.urls import reverse


from . import BaseModel
from . import Telephone


class Bagno(BaseModel):
    """ The model for Bagno object
    """
    class Meta:
        verbose_name = _('Bagno')
        verbose_name_plural = _('Bagni')
        app_label = 'bagni'

    description = RichTextField(blank=True, max_length=350, verbose_name=_("Description"),
                                   validators = [MaxLengthValidator(350)])
    number = models.CharField(max_length=30, blank=True, verbose_name=_("Number"))
    languages = models.ManyToManyField("Language", blank=True, related_name='bagni', verbose_name=_("Languages"))
    services = models.ManyToManyField("Service", blank=True, related_name='bagni', verbose_name=_("Facilities"))
    address = models.CharField(max_length=100, blank=True, verbose_name=_("Address"))
    neighbourhood = models.ForeignKey("Neighbourhood", null=True, related_name='bagni', verbose_name=_("Neighbourhood"), on_delete=models.SET_NULL)
    mail = models.EmailField(max_length=50, blank=True, verbose_name=_("Mail"))
    site = models.URLField(max_length=75, blank=True, verbose_name=_("Website"))
    point = models.PointField(srid=4326, geography=True, null=True, blank=True, verbose_name=_("Coordinates"))
    accepts_booking = models.BooleanField(null=False, blank=False,
                                          default=True, verbose_name=_("Accept booking"))


    def index_text(self):
        """ Text indexed for fulltext search (the what field)
        """
        elems = [self.name, self.number, self.description, self.address, ]
        cities = self.index_cities(field="name").split("#")
        services = self.index_services(field="name").split("#")
        elems.extend(cities)
        elems.extend(services)
        return str(" ".join(elems))

    def index_services(self, field='slug', sep="#"):
        """ Returns a string representing all the bagno services separated by
            the sep val.
            Needed to index the services as listid in whoosh and have facets
        """
        return str(sep.join([getattr(s, field) for s in self.services.all()]))


    def index_languages(self, field='slug', sep="#"):
        """ Returns a string representing all the bagno spoken languages separated by
            the sep val.
            Needed to index the languages as listid in whoosh and have facets
        """
        return str(sep.join([getattr(l, field) for l in self.languages.all()]))

    def index_cities(self, sep="#", field="slug"):
        cities = []
        if self.neighbourhood:
            cities.append(getattr(self.neighbourhood, field))
            if self.neighbourhood.municipality:
                cities.append(getattr(self.neighbourhood.municipality, field))
                if self.neighbourhood.municipality.district:
                    cities.append(getattr(self.neighbourhood.municipality.district, field))
        return str(sep.join(cities))

    def index_features(self):
        """ Returns a dictionary representing the whoosh entry for
            the current object in the index
        """
        return dict(id=str(self.id),
                    text=self.index_text(),
                    services=self.index_services(),
                    languages=self.index_languages(),
                    )

    def get_list_display_telephone_numbers(self):
        return " ~ ".join([t.name + ": " + t.number for t in self.telephones.all()])

    def get_ordered_telephones(self):
        return sorted(
                list(self.telephones.exclude(number=u'')),
                key = lambda x: Telephone.TELEPHONE_ORDERING.get(x.name, 7)
                )

    def get_complete_name(self):
        res = self.name
        if self.number:
            res += " - n. %s" % self.number
        res += " - %s" % self.address
        return res

    def get_absolute_url(self):
        return reverse("bagno", args=[self.neighbourhood.slug, self.slug])

    def get_edit_url(self):
        return reverse("bagno-edit", args=[self.neighbourhood.slug, self.slug])

    def get_contactform_url(self):
        return reverse("bagno-contacts", args=[self.neighbourhood.slug, self.slug])

    def get_booking_url(self):
        return reverse("bagno-booking", args=[self.neighbourhood.slug, self.slug])

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

    def get_nearest_managed_alternatives(self, count=2):
        bagni_managed = Bagno.objects.filter(managers__isnull=False).exclude(slug="test")
        sorted_bagni = bagni_managed.distance(self.point).order_by('distance')
        if len(sorted_bagni) > count:
            return sorted_bagni[:count]
        return sorted_bagni
