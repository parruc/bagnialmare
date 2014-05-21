#from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.views.generic.base import View

from models import NewsletterSubscription, NewsletterTarget

# Create your views here.
class SubscribeNewsletter(View):
    """ View for the newsletter subscription
    """

    def dispatch(self, request, *args, **kwargs):
        email = kwargs.get("email", "")
        target_slug = kwargs.get("slug", "")
        target = NewsletterTarget.objects.get(slug=target_slug)
        subscription, created = NewsletterSubscription.objects.get_or_create(email=email, target=target)
        if not created:
            messages.add_message(self.request, messages.WARNING, _("Subscription for email '%s' and target '%s' already exists" % (email, target_slug)))
        else:
            messages.add_message(self.request, messages.INFO, _("Subscription done for email '%s' and target '%s'" % (email, target_slug)))
        return redirect("homepage")


class UnsubscribeNewsletter(View):
    """ View for the newsletter unsubscribe
    """

    def dispatch(self, request, **kwargs):
        hash_to_remove = kwargs.get("hash", "")
        if hash_to_remove:
            subscription = NewsletterSubscription.objects.get(hash_field=hash_to_remove)
            subscription_data = (subscription.email, subscription.target.name)
            subscription.delete()
            messages.add_message(self.request, messages.INFO, _("Subscription removed for email %s and target %s" % subscription_data))
        else:
            messages.add_message(self.request, messages.ERROR, _("Cant find the hash to unsubscribe"))
        return redirect("homepage")




