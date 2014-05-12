from django.contrib import admin

import models

class UserFeedbackAdmin(admin.ModelAdmin):
    list_display = ['email', 'created', 'bagno', 'notified']

admin.site.register(models.UserFeedback, UserFeedbackAdmin)

