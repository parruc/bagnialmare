# -*- coding: utf-8 -*-
from modeltranslation.translator import translator, TranslationOptions
from . import models


class NewsletterTarget(TranslationOptions):
    fields = []

translator.register(models.NewsletterTarget, NewsletterTarget)


class NewsletterTemplate(TranslationOptions):
    fields = []

translator.register(models.NewsletterTemplate, NewsletterTemplate)

class NewsletterSubscription(TranslationOptions):
    fields = []

translator.register(models.NewsletterSubscription, NewsletterSubscription)


class Newsletter(TranslationOptions):
    fields = []

translator.register(models.Newsletter, Newsletter)
