import zmq
from datetime import datetime

from django.core.mail import EmailMultiAlternatives
from django.core.mail import get_connection
from django.conf import settings

from ..models import Newsletter, NewsletterStatus


def offload_mass_html_mail(subject, text_content, html_content, recipients, pk, from_email=None, test=False):
    context = zmq.Context()
    client = context.socket(zmq.REQ)
    client.connect(settings.MAILOFFLOADER_SOCKET) #aggiunta in settings.py
    #occhio qui quello che mandiamo deve essere serizlizable come json!
    client.send_json(dict(subject=subject,
                          text_content=text_content,
                          html_content=html_content,
                          recipients=recipients,
                          pk=pk,
                          from_email=from_email,
                          test=test))
    client.recv() #questa serve per essere sicuri che il msg sia stato ricevuto
    #now the server will import the 'send_mass_html_method' below and call it with given arguments
    return True


def send_mass_html_mail(subject, text_content, html_content, recipients, pk, from_email=None, test=False):
    if test:
        connection = get_connection(settings.MASS_EMAIL_TEST_BACKEND)
    else:
        connection = get_connection(settings.MASS_EMAIL_BACKEND)
    from_email = from_email or settings.DEFAULT_FROM_EMAIL

    messages = []
    for recipient in recipients:
        message = EmailMultiAlternatives(subject, text_content, from_email, [recipient,])
        message.attach_alternative(html_content, "text/html")
        messages.append(message)

    sent_count = connection.send_messages(messages)

    newsletter = Newsletter.objects.get(pk=pk)
    newsletter.status = NewsletterStatus.SENT
    newsletter.sent_count = sent_count
    newsletter.sent_to = "; ".join(recipients)
    newsletter.sent_on = datetime.now()
    newsletter.save()
    return sent_count
