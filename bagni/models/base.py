# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _

import autoslug


class BaseModel(models.Model):

    class Meta:
        app_label = 'bagni'
        abstract = True

    name = models.CharField(max_length=100,
                            verbose_name=_("Name"),)
    slug = autoslug.AutoSlugField(max_length=50,
                                  populate_from='name',
                                  verbose_name=_("Slug"),
                                  unique=True,
                                  editable=True,)

    def natural_key(self):
        return (self.slug,)

    def get_by_natural_key(self, slug):
        return self.get(slug=slug)

    def __unicode__(self):
        return self.name
