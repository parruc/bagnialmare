from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from managers.models import Manager

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class ManagerInline(admin.StackedInline):
    model = Manager
    can_delete = False

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (ManagerInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
