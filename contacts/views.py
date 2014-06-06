# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.template.loader import get_template
from django.template import Context
from django.views.generic.edit import FormView

from .forms import ContactForm

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class ContactView(FormView):

    template_name = "contacts/contacts.html"
    form_class = ContactForm
    success_url = "/"
    success_message = _("Thanks for contacting us. We will asnwer you as soon as possible.")
    submit_url = "."
    recipients = []
    admin_emails = [email[1] for email in settings.ADMINS]

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        subject = "Richiesta informazioni"
        sender = form.cleaned_data['sender']
        from_email = "info@bagnialmare.com"
        bcc = []


        if self.recipients:
            # If there is already a recipient put us in BCC
            bcc = self.admin_emails
        else:
            #else we are the receivers directly
            self.recipients = self.admin_emails
        try:
            t = get_template("contacts/email.txt")
            c = Context({"message": form.cleaned_data['message'], })
            message = t.render(c)

            t = get_template("contacts/subject.txt")
            c = Context({"subject": subject, })
            subject = t.render(c).strip()

            email = EmailMessage(subject=subject, body=message,from_email=from_email,
                                 to=self.recipients, bcc=bcc, headers={'Reply-To': sender})
            email.send()
            messages.add_message(self.request, messages.INFO, self.success_message)
        except Exception as e:
            logger.error("Error '%s' sending the mail" % str(e))
            messages.add_message(self.request, messages.ERROR,
                _("Error sending the mail: Contact us at \
                   info at bagnialmare dot com to inform \
                   us about the error. Thanks"))
        return super(ContactView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(ContactView, self).get_context_data(*args, **kwargs)
        context.update({"submit_url": self.submit_url})
        return context

