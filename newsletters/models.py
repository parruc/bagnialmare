from django.db import models
from django.utils.translation import ugettext_lazy as _
from ckeditor.fields import RichTextField

# Create your models here.

class NewsletterTarget(models.Model):
    """ The target for Newsletter objects
    """
    class Meta:
        verbose_name = _('Newsletter target')
        verbose_name_plural = _('Newsletter targets')

    name = models.CharField(max_length=100, verbose_name=_("Name"))
    #occhio che filter e una funzione builtin in python!!
    filter = models.CharField(max_length=500, verbose_name=_("Filter"))

    def __unicode__(self):
        return self.name


class NewsletterTemplate(models.Model):
    """ The template for Newsletter objects
    """
    class Meta:
        verbose_name = _('Newsletter tempalte')
        verbose_name_plural = _('Newsletter tempalte')

    name = models.CharField(max_length=100, verbose_name=_("Name"))
    path = models.CharField(max_length=100, verbose_name=_("Path"))

    def __unicode__(self):
        return self.name


class Newsletter(models.Model):
    """ The model for Newsletter object
    """
    class Meta:
        verbose_name = _('Newsletter')
        verbose_name_plural = _('Newsletters')

    subject = models.CharField(max_length=100, verbose_name=_("Subject"))
    text = RichTextField(max_length=2000, verbose_name=_("Text"))
    sent_to = models.TextField(editable=False, null=True, blank=True)
    sent_on = models.TimeField(editable=False, null=True, blank=True)
    target = models.ForeignKey("NewsletterTarget", related_name="newsletters", verbose_name=_("Target"),)
    template = models.ForeignKey("NewsletterTemplate", related_name="newsletters", verbose_name=_("Template"),)

    def __unicode__(self):
        return self.subject
