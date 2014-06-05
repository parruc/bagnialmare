import json

from django import http
from django.views.generic import View

from .models import NewsletterSubscription, NewsletterTarget



class JSONResponseMixin(object):
    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        # ...but on the other side serializing django objects to dictionaries
        # is quite easy and is enough for 95% of usecases ;-)
        return json.dumps(context)


# Create your views here.
class SubscribeNewsletter(JSONResponseMixin, View):
    """ View that subscribes users for a specific target starting from the target slug and email
    """

    def dispatch(self, request, *args, **kwargs):
        email = kwargs.get("email", "")
        target_slug = kwargs.get("slug", "")
        context = {"result": "KO"}
        try:
            target = NewsletterTarget.objects.get(slug=target_slug)
            subscription, created = NewsletterSubscription.objects.get_or_create(email=email, target=target)
        except:
            return self.render_to_response(context)

        if not created:
            context = {"result": "EXISTS"}
            #messages.add_message(self.request, messages.WARNING, _("Subscription for email '%s' and target '%s' already exists" % (email, target_slug)))
        else:
            context = {"result": "OK"}
            #messages.add_message(self.request, messages.INFO, _("Subscription done for email '%s' and target '%s'" % (email, target_slug)))
        return self.render_to_response(context)


class UnsubscribeNewsletter(JSONResponseMixin, View):
    """ View that unsubscribe users from a specific target starting from the subscription hash
    """

    def dispatch(self, request, *args, **kwargs):
        hash_to_remove = kwargs.get("hash", "")
        context = {"result": "KO"}
        if hash_to_remove:
            try:
                subscription = NewsletterSubscription.objects.get(hash_field=hash_to_remove)
            except:
                context = {"result": "NOTEXISTS"}
            else:
                subscription.delete()
                context = {"result": "OK"}
        return self.render_to_response(context)




