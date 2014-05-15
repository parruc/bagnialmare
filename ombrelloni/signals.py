from django.db.models import signals
from django.conf import settings
from django.core.mail import send_mail
from authauth.models import Manager
from bagni.models import Bagno


def mail_admin(sender, instance, created, **kwargs):
    admin_emails = [email[1] for email in settings.ADMINS]
    action = "modified"
    if created:
        action = "created"

    subject = "[bagnialmare.com updates]"
    message = "{model} {title} {action}".format(
        model=instance._meta.verbose_name.title(),
        title=repr(instance),
        action=action)
    send_mail(subject, message, "info@bagnialmare.com", admin_emails)

signals.post_save.connect(mail_admin, sender=Manager)
signals.post_save.connect(mail_admin, sender=Bagno)
