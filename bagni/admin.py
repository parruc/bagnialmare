from django.contrib import admin
from django.contrib.gis.admin import GeoModelAdmin
from modeltranslation.admin import TranslationAdmin
from . import models


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
    search_fields = ['name', 'services__name']
    list_filter = ['neighbourhood__municipality__district', 'neighbourhood__municipality', 'neighbourhood', 'services']
    list_display = ['name', 'number', 'mail', 'site', 'get_list_display_telephone_numbers']
    inlines = [
            ImageInline,
            TelephoneInline,
            ]

admin.site.register(models.Bagno, BagnoAdmin)
