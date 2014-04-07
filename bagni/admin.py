from django.contrib import admin
from django.contrib.gis.admin import GeoModelAdmin
from modeltranslation.admin import TranslationAdmin
import models


class DistrictAdmin(TranslationAdmin, GeoModelAdmin, admin.ModelAdmin):
    pass


admin.site.register(models.District, DistrictAdmin)


class MunicipalityAdmin(TranslationAdmin, GeoModelAdmin, admin.ModelAdmin):
    pass


admin.site.register(models.Municipality, MunicipalityAdmin)


class NeighbourhoodAdmin(TranslationAdmin, GeoModelAdmin, admin.ModelAdmin):
    pass


admin.site.register(models.Neighbourhood, NeighbourhoodAdmin)


class ServiceAdmin(TranslationAdmin, GeoModelAdmin, admin.ModelAdmin):
    pass


admin.site.register(models.Service, ServiceAdmin)


class ServiceCategoryAdmin(TranslationAdmin, GeoModelAdmin, admin.ModelAdmin):
    pass


admin.site.register(models.ServiceCategory, ServiceCategoryAdmin)


class LanguageAdmin(TranslationAdmin, GeoModelAdmin, admin.ModelAdmin):
    pass


admin.site.register(models.Language, LanguageAdmin)


class TelephoneAdmin(TranslationAdmin, GeoModelAdmin, admin.ModelAdmin):
    pass


admin.site.register(models.Telephone, TelephoneAdmin)


class TelephoneInline(admin.StackedInline):
    model = models.Telephone


class ImageAdmin(TranslationAdmin, GeoModelAdmin, admin.ModelAdmin):
    pass


admin.site.register(models.Image, ImageAdmin)


class ImageInline(admin.StackedInline):
    model = models.Image


class BagnoAdmin(TranslationAdmin, GeoModelAdmin, admin.ModelAdmin):
    inlines = [
            ImageInline,
            TelephoneInline,
            ]

admin.site.register(models.Bagno, BagnoAdmin)
