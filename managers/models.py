from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from bagni.models import Bagno

# Create your models here.


class Manager(models.Model):
    user = models.OneToOneField(User, null=True, blank=True)
    bagni = models.ManyToManyField(Bagno, null=True, blank=True)
    privacy = models.BooleanField(default=True, help_text=_(u"Termini della privacy da inserire"))
