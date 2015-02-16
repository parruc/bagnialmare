from django.contrib import admin

from .models import Booking


class BookingAdmin(admin.ModelAdmin):
    list_display = ['bagno', 'start', 'end', 'umbrellas', 'sunbeds', 'email', 'mobile']

admin.site.register(Booking, BookingAdmin)
