from django.utils import translation
from django.contrib import admin
from django.contrib import messages
from django.template import Context
from django.template.loader import get_template
from django.template.defaultfilters import striptags
from modeltranslation.admin import TranslationAdmin

from . import models
from .mail.helpers import offload_mass_html_mail


def send_test_newsletter(modeladmin, request, queryset):
    _send_newsletter(modeladmin, request, queryset, test=True)


def send_newsletter(modeladmin, request, queryset):
    _send_newsletter(modeladmin, request, queryset, test=False)


def _send_newsletter(modeladmin, request, queryset, test):
    if queryset.count() != 1:
        modeladmin.message_user(request, "Can send only one newsletter at a time",
                                      level=messages.ERROR, extra_tags='', fail_silently=False)
        return
    obj = queryset.first()
    if obj.status in ("sent", "sending"):
        modeladmin.message_user(request, "You already sent this newsletter",
                                      level=messages.ERROR, extra_tags='', fail_silently=False)
        return

    if obj.status == "sending":
        modeladmin.message_user(request, "You already sent this newsletter",
                                      level=messages.ERROR, extra_tags='', fail_silently=False)
        return

    text_content = striptags(obj.text)

    # Get template and compile it
    try:
        t = get_template(obj.template.path)
        c = Context({"subject": obj.subject, "text": obj.text})

        translation.activate("it")
        html_content = t.render(c)
        translation.deactivate()
    except Exception as e:
        modeladmin.message_user(request, "Error %s trying to render template %s" % (str(e), obj.template.path),
                                level=messages.ERROR, extra_tags='', fail_silently=False)
        return

    #Get target users email
    recipients = [s.email for s in obj.target.subscribers.all()]

    try:
        sent_mail = offload_mass_html_mail(subject=obj.subject,
                            text_content=text_content,
                            html_content=html_content,
                            recipients=recipients,
                            pk=obj.pk,
                            test=test,)

    except Exception as e:
        modeladmin.message_user(request, "Error %s trying send emails" % str(e),
                                  level=messages.ERROR, extra_tags='', fail_silently=False)
        return
    if not sent_mail:
        modeladmin.message_user(request, "Failed to send send emails",
                                  level=messages.ERROR, extra_tags='', fail_silently=False)
        return
    obj.status = models.NewsletterStatus.SENDING
    obj.save()
    modeladmin.message_user(request, "Sent emails",
                            level=messages.INFO, extra_tags='', fail_silently=False)
        

send_newsletter.short_description = "Send selected newsletter"
send_test_newsletter.short_description = "Test selected newsletter"

class NewsletterTargetAdmin(TranslationAdmin, admin.ModelAdmin):
    pass

admin.site.register(models.NewsletterTarget, NewsletterTargetAdmin)


class NewsletterTemplateAdmin(TranslationAdmin, admin.ModelAdmin):
    pass

admin.site.register(models.NewsletterTemplate, NewsletterTemplateAdmin)

class NewsletterSubscriptionAdmin(TranslationAdmin, admin.ModelAdmin):
    pass

admin.site.register(models.NewsletterSubscription, NewsletterSubscriptionAdmin)

class NewsletterAdmin(TranslationAdmin, admin.ModelAdmin):
    actions = [send_newsletter, send_test_newsletter]
    readonly_fields=('status', 'sent_on', 'sent_to', 'sent_count')
    list_display = ['name', 'status', 'target', 'template', ]

admin.site.register(models.Newsletter, NewsletterAdmin)
