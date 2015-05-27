from uuid import uuid4

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from ckeditor.fields import RichTextField
from bagni.models import BaseModel


class NewsletterStatus:
    NEW = "new"
    SENT = "sent"
    SENDING = "sending"

class NewsletterUser(models.Model):
    """ The target for Newsletter objects
    """
    class Meta:
        verbose_name = _('Newsletter user')
        verbose_name_plural = _('Newsletter users')

    user = models.OneToOneField(User, related_name='newsletter_user')
    old_email = models.EmailField(editable=False)

    def __unicode__(self):
        return self.user.username

class NewsletterTarget(BaseModel):
    """ The target for Newsletter objects
    """
    class Meta:
        verbose_name = _('Newsletter target')
        verbose_name_plural = _('Newsletter targets')

    def __unicode__(self):
        return self.name


class NewsletterTemplate(BaseModel):
    """ The template for Newsletter objects
    """
    class Meta:
        verbose_name = _('Newsletter tempalte')
        verbose_name_plural = _('Newsletter tempalte')

    path = models.CharField(max_length=100, verbose_name=_("Path"))

    def __unicode__(self):
        return self.name


class Newsletter(BaseModel):
    """ The model for Newsletter object
    """
    class Meta:
        verbose_name = _('Newsletter')
        verbose_name_plural = _('Newsletters')

    subject = models.CharField(max_length=100, verbose_name=_("Subject"))
    text = RichTextField(max_length=2000, verbose_name=_("Text"))
    sent_to = models.TextField(editable=False, null=True, blank=True)
    sent_on = models.TimeField(editable=False, null=True, blank=True)
    sent_count = models.IntegerField(editable=False, null=True, blank=True)
    status = models.CharField(editable=False, default=NewsletterStatus.NEW, max_length=10, verbose_name=_("Status"))
    target = models.ForeignKey("NewsletterTarget", related_name="newsletters", verbose_name=_("Target"),)
    template = models.ForeignKey("NewsletterTemplate", related_name="newsletters", verbose_name=_("Template"),)

    def __unicode__(self):
        return self.subject

class NewsletterSubscription(models.Model):
    class Meta:
        verbose_name = _('Newsletter subscriber')
        verbose_name_plural = _('Newsletter subscribers')
        unique_together = ("email", "target", )

    email = models.EmailField(verbose_name=_("Email"))
    target = models.ForeignKey("NewsletterTarget", related_name="subscribers", verbose_name=_("Targets"))
    hash_field = models.CharField(editable=False, blank=True, max_length=40, unique=True)

    def save(self, *args, **kwargs):
        if not self.hash_field:
            self.hash_field = uuid4().hex
        super(NewsletterSubscription, self).save(*args, **kwargs)
