from django.db.models import signals
from django.contrib.auth.models import User
from models import NewsletterSubscription
from models import NewsletterUser


def change_newsletters_user_email(sender, instance, created, **kwargs):
    email = instance.email
    if not hasattr(instance, "newsletter_user"):
        newsletter_user = NewsletterUser(user=instance, old_email=email)
        newsletter_user.save()
    old_email = instance.newsletter_user.old_email

    if email != old_email:
        for subscription in NewsletterSubscription.objects.filter(email=old_email):
            subscription.email = instance.email
            subscription.save()
        instance.newsletter_user.old_email = email
        instance.save()

signals.post_save.connect(change_newsletters_user_email, sender=User)
