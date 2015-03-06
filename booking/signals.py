# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.conf import settings
from django.template.loader import get_template
from django.template import Context
from django.utils.translation import ugettext as _

def _get_bagno_url(bagno):
    #TODO: shoudl we add settings.SITE_URL?
    return "http://bagnialmare.com" + bagno.get_absolute_url()

def _get_bagno_registration_url(bagno_id):
    #TODO: shoudl we add settings.SITE_URL?
    return "http://bagnialmare.com" + \
           reverse("authauth_signup") + \
           "?selected=%d" % (bagno_id)

def _send_mail_by_template(template_prefix, details, recipients):
    t = get_template("booking/" + template_prefix + "_mail_subject.txt")
    c = Context(details)
    subject = t.render(c).strip()

    t = get_template("booking/" + template_prefix + "_mail_message.txt")
    c = Context(details)
    message = t.render(c).strip()

    send_mail(subject,
              message,
              "info@bagnialmare.com",
              recipients)


def mail_for_booking(sender, instance, created, **kwargs):
    admin_emails = [email[1] for email in settings.ADMINS]
    bagno_name = instance.bagno.name
    bagno_managed = instance.bagno.is_managed()
    bagno_phones = instance.bagno.get_list_display_telephone_numbers()
    bagno_url = _get_bagno_url(instance.bagno)
    bagno_registration_url = _get_bagno_registration_url(instance.bagno.id)
    managed_state = bagno_managed and _("managed") or\
        _("not managed (WE HAVE TO CALL)")
    booking_details = dict(bagno_name=bagno_name,
                           bagno_mail=instance.bagno.mail,
                           bagno_phones=bagno_phones,
                           bagno_url=bagno_url,
                           bagno_registration_url=bagno_registration_url,
                           start=instance.start,
                           end=instance.end,
                           umbrellas=instance.umbrellas,
                           sunbeds=instance.sunbeds,
                           email=instance.email,
                           mobile=instance.mobile,
                           managed_state=managed_state)

    if bagno_managed:
        managers = instance.bagno.managers.all()
        manager_emails = [m.user.email for m in managers]
        booking_details["bagno_managers_mail"] = ", ".join(manager_emails)
        _send_mail_by_template("manager", booking_details, manager_emails)

    _send_mail_by_template("admin", booking_details, admin_emails)
    _send_mail_by_template("user", booking_details, [instance.email, ])
