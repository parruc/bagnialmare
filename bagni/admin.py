from django.contrib import admin
from django.contrib.gis.admin import GeoModelAdmin
from modeltranslation.admin import TranslationAdmin
import models

#TODO: Mettere le foreignkeys come fields inline


class DistrictAdmin(TranslationAdmin, GeoModelAdmin, admin.ModelAdmin):
    pass

class MunicipalityAdmin(TranslationAdmin, GeoModelAdmin, admin.ModelAdmin):
    pass

class ServiceAdmin(TranslationAdmin, GeoModelAdmin, admin.ModelAdmin):
    pass

class ServiceCategoryAdmin(TranslationAdmin, GeoModelAdmin, admin.ModelAdmin):
    pass

class LanguageAdmin(TranslationAdmin, GeoModelAdmin, admin.ModelAdmin):
    pass

class TelephoneAdmin(TranslationAdmin, GeoModelAdmin, admin.ModelAdmin):
    pass

class TelephoneInline(admin.StackedInline):
    model = models.Telephone

class ImageAdmin(TranslationAdmin, GeoModelAdmin, admin.ModelAdmin):
    pass

class ImageInline(admin.StackedInline):
    model = models.Image

class BagnoAdmin(TranslationAdmin, GeoModelAdmin, admin.ModelAdmin):
    inlines = [
            ImageInline,
            TelephoneInline,
            ]


admin.site.register(models.Bagno, BagnoAdmin)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.ServiceCategory, ServiceCategoryAdmin)
admin.site.register(models.Image, ImageAdmin)
admin.site.register(models.District, DistrictAdmin)
admin.site.register(models.Municipality, MunicipalityAdmin)
admin.site.register(models.Language, LanguageAdmin)
admin.site.register(models.Telephone, TelephoneAdmin)
