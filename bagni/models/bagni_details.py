# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail import ImageField
import autoslug

class Language(models.Model):
    """ List of languages available for the spoken language field in bagno
    """
    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')
        app_label = 'bagni'

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
    slug = autoslug.AutoSlugField(max_length=50,
                                  populate_from='name',
                                  verbose_name=_("Slug"),
                                  unique=True,
                                  editable=True,)
    def __unicode__(self):
        return self.name


class Telephone(models.Model):
    """ List of telephone numbers of the bagno
    """
    class Meta:
        verbose_name = _('Telephone number')
        verbose_name_plural = _('Telephone numbers')
        app_label = 'bagni'

    name = models.CharField(max_length=25)
    number = models.CharField(max_length=100)
    bagno = models.ForeignKey("Bagno", related_name="telephones", verbose_name=_("Bagno"),)
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

    def _define_filename(self, filename):
        extension = filename.split('.')[-1] or 'jpg'
        upload_filename = self.bagno.slug + '.' + extension
        upload_base_path = "images/bagni"
        upload_path = "%s/%s/%s" % (upload_base_path,
                                    self.bagno.slug,
                                    upload_filename)
        return upload_path


    name = models.CharField(max_length=50)
    description = models.TextField(max_length=2000, blank=True)
    slug = autoslug.AutoSlugField(max_length=50,
                                  populate_from='name',
                                  verbose_name=_("Slug"),
                                  unique=True,
                                  editable=True,)
    image = ImageField(upload_to=_define_filename, verbose_name=_("Image"),)
    bagno = models.ForeignKey("Bagno", related_name="images", verbose_name=_("Bagno"),)
