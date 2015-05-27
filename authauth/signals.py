# -*- coding: utf-8 -*-
from django.db.models import signals
from django.conf import settings
from django.core.mail import send_mail

MANAGER_CREATION_TEMPLATE = """
    We have a new regeistered manager!
    name: {name}
    bagno: {bagno_name} 
    link: {bagno_url}
    """

MANAGER_UPDATE_TEMPLATE = """
    Manager modified:
    name: {name}
    bagno: {bagno_name} 
    link: {bagno_url}
    """

def get_manager_mail(instance, subject, template):
    subject = "[bagnialmare.com] new manager"
    name = instance.name
    bagno = instance.bagni.first()
    if bagno:
        message = template.format(
            name = name,
            bagno_name = bagno.name,
            #TODO: should we add SITE_URL to settings?
            bagno_url = "http://bagnialmare.com" + bagno.get_absolute_url(),
        )
    else:
        message = template.format(
            name = name,
            bagno_name = "undefined",
            bagno_url = "undefined",
        )
    return subject, message

def mail_for_manager(sender, instance, created, **kwargs):
    admin_emails = [email[1] for email in settings.ADMINS]
    if created:
        subject, message = get_manager_mail(instance,
                         "[bagnialmare.com] new manager",
                         MANAGER_CREATION_TEMPLATE)
    else:
        subject, message = get_manager_mail(instance,
                         "[bagnialmare.com] manager updated",
                         MANAGER_UPDATE_TEMPLATE)
    send_mail(subject, message, "info@bagnialmare.com", admin_emails)

