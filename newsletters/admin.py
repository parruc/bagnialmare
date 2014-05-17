import ast
from datetime import datetime

from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.models import User
from django.template import Context
from django.template.loader import get_template
from django.template.defaultfilters import striptags
from modeltranslation.admin import TranslationAdmin

import models
from .mail.helpers import send_mass_html_mail


def send_newsletter(modeladmin, request, queryset):
    if queryset.count() != 1:
        modeladmin.message_user(request, "Can send only one newsletter at a time",
                                      level=messages.ERROR, extra_tags='', fail_silently=False)
        return
    obj = queryset[:1].get()
    import ipdb; ipdb.set_trace()
    if obj.sent_on:
        modeladmin.message_user(request, "You already sent this newsletter",
                                      level=messages.ERROR, extra_tags='', fail_silently=False)
        return

    text_content = striptags(obj.text)

    # Get template and compile it
    try:
        t = get_template(obj.template.path)
        c = Context({"subject": obj.subject, "text": obj.text})
        html_content = t.render(c)
    except Exception as e:
        modeladmin.message_user(request, "Error %s trying to render template %s" % (str(e), obj.template.path),
                                  level=messages.ERROR, extra_tags='', fail_silently=False)
        return

    #Get target users email
    try:
        filters = ast.literal_eval(obj.target.filter)
        users = User.objects.filter(**filters)
    except Exception as e:
        modeladmin.message_user(request, "Error %s trying to query for %s" % (str(e), obj.target.filter),
                                  level=messages.ERROR, extra_tags='', fail_silently=False)
        return
    recipients = [user.email for user in users]

    try:
        send_mass_html_mail(subject=obj.subject, text_content=text_content, html_content=html_content, recipients=recipients)
    except Exception as e:
        modeladmin.message_user(request, "Error %s trying send emails" % (str(e), obj.template.path),
                                  level=messages.ERROR, extra_tags='', fail_silently=False)
        return

    obj.sent_on = datetime.now()
    obj.sent_to = "; ".join(recipients)
    obj.save()

    modeladmin.message_user(request, "You have sent the selected newsletter",
                                      level=messages.INFO, extra_tags='', fail_silently=False)


send_newsletter.short_description = "Send selected newsletter"

class NewsletterTargetAdmin(TranslationAdmin, admin.ModelAdmin):
    pass

admin.site.register(models.NewsletterTarget, NewsletterTargetAdmin)


class NewsletterTemplateAdmin(TranslationAdmin, admin.ModelAdmin):
    pass

admin.site.register(models.NewsletterTemplate, NewsletterTemplateAdmin)


class NewsletterAdmin(TranslationAdmin, admin.ModelAdmin):
    actions = [send_newsletter]

admin.site.register(models.Newsletter, NewsletterAdmin)
