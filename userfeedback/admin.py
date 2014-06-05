from django.contrib import admin

from . import models

class UserFeedbackAdmin(admin.ModelAdmin):
    list_display = ['email', 'created', 'bagno', 'notified']

admin.site.register(models.UserFeedback, UserFeedbackAdmin)

