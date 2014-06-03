import os
import logging
logging.basicConfig(level=logging.INFO)
import sys
import threading

import zmq
import django

if __name__ == "__main__":
    logger = logging.getLogger(__module__)
    settings = os.getenv("DJANGO_SETTINGS_MODULE")
    if not settings:
        logger.error("this process must live in a django environment")
        sys.exit(-1)
    if sys.argv and len(sys.argv) > 1:
        if os.path.exists(sys.argv[1]):
            sys.path.insert(0, sys.argv[1])
            logger.info("insert %s into path" % (sys.argv[1],))
    logger.info("resulting ENV:")
    logger.info(os.environ)
    logger.info("resulting SYS.PATH:")
    logger.info(sys.path)
    from django.conf import settings
    from newsletters.mail.helpers import send_mass_html_mail
    context = zmq.Context()
    server = context.socket(zmq.REP)
    server.bind(settings.MAILOFFLOADER_SOCKET)
    while True:
        msg = server.recv_json()
        #send_mass_html_mail(msg['subject'], msg['text_content'], msg['html_content'], msg['recipients'], msg['from_email'], msg['test']
        logger.DEBUG("received: %s" % (msg,))
        server.send_string("ack")
    sys.exit(0)

