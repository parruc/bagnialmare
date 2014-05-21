from django.db.models import signals
from django.contrib.auth.models import User
from models import NewsletterSubscription


def change_newsletters_user_email(sender, instance, created, **kwargs):
    old_email = instance.newsletter_user.old_email
    new_email = instance.email
    if new_email != old_email:
        for subscription in NewsletterSubscription.objects.filter(email=old_email):
            subscription.email = instance.email
            subscription.save()
        instance.newsletter_user.old_email = new_email
        instance.save()

signals.post_save.connect(change_newsletters_user_email, sender=User)
