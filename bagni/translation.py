# -*- coding: utf-8 -*-
from modeltranslation.translator import translator, TranslationOptions
from . import models


class BagnoTranslationOptions(TranslationOptions):
    #fields = ('name', 'description', 'slug',  'address',)
    fields = ('description',)

translator.register(models.Bagno, BagnoTranslationOptions)


class ServiceTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'aliases', 'seo_name', 'slug',)

translator.register(models.Service, ServiceTranslationOptions)


class DistrictTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'slug',)

translator.register(models.District, DistrictTranslationOptions)


class MunicipalityTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'slug',)

translator.register(models.Municipality, MunicipalityTranslationOptions)

class NeighbourhoodTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'slug',)

translator.register(models.Neighbourhood, NeighbourhoodTranslationOptions)


class ServiceCategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'slug',)

translator.register(models.ServiceCategory, ServiceCategoryTranslationOptions)


class LanguageTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'slug',)

translator.register(models.Language, LanguageTranslationOptions)


class TelephoneTranslationOptions(TranslationOptions):
    fields = ()

translator.register(models.Telephone, TelephoneTranslationOptions)


class ImageTranslationOptions(TranslationOptions):
    fields = ()

translator.register(models.Image, ImageTranslationOptions)

