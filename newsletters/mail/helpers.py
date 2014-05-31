from django.core.mail import EmailMultiAlternatives
from django.core.mail import get_connection
from django.conf import settings


def send_mass_html_mail(subject, text_content, html_content, recipients, from_email=None, test=False):
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

    return connection.send_messages(messages)
