# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.views.generic.edit import FormView

from forms import ContactForm


class ContactView(FormView):

    template_name = "contacts/contacts.html"
    form_class = ContactForm
    success_url = "/"

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        sender = form.cleaned_data['sender']
        from_email = "info@bagnialmare.com"
        cc_myself = form.cleaned_data['cc_myself']

        recipients = [email[1] for email in settings.ADMINS]
        if cc_myself:
            email = EmailMessage(subject, message, from_email,
            [sender, ])
            email.send()
        try:
            email = EmailMessage(subject, message, from_email,
            recipients, headers={'Reply-To': sender})
            email.send()
            messages.add_message(self.request, messages.INFO,
                _("Thanks for contacting us. We will asnwer you as soon as possible."))
        except:
            messages.add_message(self.request, messages.ERROR,
                _("Error sending the mail: Contact me at \
                   info at bagnialmare dot com to inform \
                   us about the error. Thanks"))
        return super(ContactView, self).form_valid(form)


