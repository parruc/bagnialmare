# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
import autoslug

from sorl.thumbnail import ImageField

from . import BaseModel

class Language(BaseModel):
    """ List of languages available for the spoken language field in bagno
    """
    class Meta:
        verbose_name = _('Spoken language')
        verbose_name_plural = _('Spoken languages')
        app_label = 'bagni'

    description = models.TextField(max_length=2000, verbose_name=_("Description"))


class Telephone(models.Model):
    """ List of telephone numbers of the bagno
    """

    class Meta:
        verbose_name = _('Telephone number')
        verbose_name_plural = _('Telephone numbers')
        app_label = 'bagni'

    TELEPHONE_NAME_CHOICES = (
            ('mob', _("Mobile number")),
            ('tel', _("Telephone number")),
            ('fax', _("Fax number")),
            ('win', _("Winter number")),
            )

    TELEPHONE_ORDERING = {
                           'mob' : 1,
                           'tel' : 5,
                           'fax' : 10,
                           'win' : 15,
                        }

    name = models.CharField(max_length=100,
                            choices = TELEPHONE_NAME_CHOICES,
                            verbose_name=_("Telephone"),)

    slug = autoslug.AutoSlugField(max_length=50,
                                  populate_from='name',
                                  verbose_name=_("Slug"),
                                  unique=True,
                                  editable=True,)

    number = models.CharField(max_length=100, blank=True,  verbose_name=_("Number"))

    bagno = models.ForeignKey("Bagno", related_name="telephones", verbose_name=_("Bagno"),)

    def natural_key(self):
        return (self.slug,)

    def get_by_natural_key(self, slug):
        return self.get(slug=slug)

    def __unicode__(self):
        return self.name


class Image(models.Model):
    """ Model used for the bagno images
        TODO: inline in admin form of bagno?
    """
    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
        app_label = 'bagni'

    name = models.CharField(max_length=100,
                            verbose_name=_("Title"),)

    slug = autoslug.AutoSlugField(max_length=50,
                                  populate_from='name',
                                  verbose_name=_("Slug"),
                                  unique=True,
                                  editable=True,)

    def _define_filename(self, filename):
        extension = filename.split('.')[-1] or 'jpg'
        upload_filename = self.slug + '.' + extension
        upload_base_path = "images/bagni"
        upload_path = "%s/%s/%s" % (upload_base_path,
                                    self.bagno.slug,
                                    upload_filename)
        return upload_path

    description = models.TextField(max_length=2000, blank=True, verbose_name=_("Description"))
    image = ImageField(upload_to=_define_filename, verbose_name=_("Image"),)
    bagno = models.ForeignKey("Bagno", related_name="images", verbose_name=_("Bagno"),)

    def natural_key(self):
        return (self.slug,)

    def get_by_natural_key(self, slug):
        return self.get(slug=slug)

    def __unicode__(self):
        return self.name

