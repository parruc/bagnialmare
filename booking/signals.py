# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import get_template
from django.template import Context


def mail_for_booking(sender, instance, created, **kwargs):
    admin_emails = [email[1] for email in settings.ADMINS]
    bagno_name = instance.bagno.name
    booking_details = dict(bagno_name=bagno_name,
                           start=instance.start,
                           end=instance.end,
                           umbrellas=instance.umbrellas,
                           sunbeds=instance.sunbeds,
                           email=instance.email,
                           mobile=instance.mobile,)

    t = get_template("booking/admin_mail_subject.txt")
    c = Context({"bango_name": bagno_name, })
    admin_subject = t.render(c).strip()

    t = get_template("booking/admin_mail_message.txt")
    c = Context(booking_details)
    admin_message = t.render(c).strip()

    send_mail(admin_subject,
              admin_message,
              "info@bagnialmare.com",
              admin_emails)

    if instance.bagno.is_managed():
        t = get_template("booking/manager_mail_subject.txt")
        c = Context({"bango_name": bagno_name, })
        manager_subject = t.render(c).strip()

        t = get_template("booking/manager_mail_message.txt")
        c = Context(booking_details)
        manager_message = t.render(c).strip()

        managers = instance.bagno.managers.all()
        magager_recipients = [m.user.email for m in managers]

        send_mail(manager_subject,
                  manager_message,
                  "info@bagnialmare.com",
                  magager_recipients)
