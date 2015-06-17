# -*- coding: utf-8 -*-
from django.db.models import signals
from django.conf import settings
from django.core.mail import send_mail

BAGNO_UPDATE_TEMPLATE = u"""
Bagno: {name}
action: {action}
url: {url}
"""

def mail_for_bagno(sender, instance, created, **kwargs):
    admin_emails = [email[1] for email in settings.ADMINS]
    subject = "[bagnialmare.com] bagno updated"
    if created:
        action = "created"
    else:
        action = "updated"
    name = instance.name
    #TODO: should we add settings.SITE_URL ?
    url = "http://bagnialmare.com" + instance.get_absolute_url()
    message = BAGNO_UPDATE_TEMPLATE.format(
        name = name,
        action = action,
        url = url,
    )
    send_mail(subject, message, "info@bagnialmare.com", admin_emails)

