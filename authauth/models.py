from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from bagni.models import Bagno

# Create your models here.


class Manager(models.Model):

    name = models.CharField(max_length=50,
                            verbose_name=_("Name"),
    )

    surname = models.CharField(max_length=50,
                               verbose_name=_("Surname"),
    )

    user = models.OneToOneField(User,
                                null=True,
                                blank=True,
                                on_delete=models.CASCADE,
    )

    bagni = models.ManyToManyField(Bagno,
                                   null=True, blank=True,
                                   related_name='managers',
    )

    privacy = models.BooleanField(default=True,
                                  null=False, blank=False,
                                  verbose_name=_("Privacy terms"),
                                  help_text=_(u"Privacy terms definition")
    )

    tos = models.BooleanField(default=True,
                              null=False, blank=False,
                              verbose_name=_("Terms of service "),
                              help_text=_(u"Terms of service definition")
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def can_edit(self, obj):
        if obj in self.bagni.all():
            return True
        return False

    def natural_key(self):
        return (self.user.email, )

    def get_by_natural_key(self, email):
        return self.get(user__email=email)

    def __unicode__(self):
        return self.name

def display_user(user):
    return user.email

