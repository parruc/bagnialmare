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
    submit_url = "."
    recipients = []


    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        subject = "[bagnialmare.com]"
        message = form.cleaned_data['message']
        sender = form.cleaned_data['sender']
        from_email = "info@bagnialmare.com"
        bcc = []
        recipients = []
        admin_emails = [email[1] for email in settings.ADMINS]

        if self.recipients:
            # If there is already a recipient put us in BCC
            bcc = admin_emails
        else:
            #else we are the receivers directly
            self.recipients = admin_emails
        try:
            email = EmailMessage(subject, message, from_email,
            recipients, bcc, headers={'Reply-To': sender})
            email.send()
            messages.add_message(self.request, messages.INFO,
                _("Thanks for contacting us. We will asnwer you as soon as possible."))
        except:
            messages.add_message(self.request, messages.ERROR,
                _("Error sending the mail: Contact me at \
                   info at bagnialmare dot com to inform \
                   us about the error. Thanks"))
        return super(ContactView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(ContactView, self).get_context_data(*args, **kwargs)
        context.update({"submit_url": self.submit_url})
        return context

