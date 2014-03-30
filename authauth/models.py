from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from bagni.models import Bagno

# Create your models here.


class Manager(models.Model):

    user = models.OneToOneField(User,
        null=True, blank=True,
    )
    bagni = models.ManyToManyField(Bagno,
        null=True, blank=True,
        related_name='managers',
    )
    privacy = models.BooleanField(default=True,
        null=False, blank=False,
        help_text=_(u"Privacy terms")
    )

    tos = models.BooleanField(default=True,
        null=False, blank=False,
        help_text=_(u"Terms of service")
    )

    def can_edit(self, obj):
        if obj in self.bagni.all():
            return True
        return False
