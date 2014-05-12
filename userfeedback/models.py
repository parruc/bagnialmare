from django.contrib.gis.db import models

class UserFeedback(models.Model):
    email = models.EmailField(blank=True, null=True)
    created = models.DateTimeField(auto_now=True, auto_now_add=True)
    notified = models.BooleanField(default=False)
    bagno = models.ForeignKey('bagni.Bagno', blank=True, null=True,
                              on_delete = models.SET_NULL,
                              related_name = 'feedbacks')

    def natural_key(self):
        return (self.created, )

