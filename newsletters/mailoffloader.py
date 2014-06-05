import os
import sys
import zmq

import logging
logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    logger = logging.getLogger("mailoffloader")
    settings_module = os.getenv("DJANGO_SETTINGS_MODULE")
    if not settings_module:
        logger.error("this process must live in a django environment")
        sys.exit(-1)
    if sys.argv and len(sys.argv) > 1:
        if os.path.exists(sys.argv[1]):
            sys.path.insert(0, sys.argv[1])
            logger.debug("insert %s into path" % (sys.argv[1],))
    logger.debug("resulting ENV:")
    logger.debug(os.environ)
    logger.debug("resulting SYS.PATH:")
    logger.debug(sys.path)
    from django.conf import settings
    logger.debug("found socket: %s" % settings.MAILOFFLOADER_SOCKET)
    context = zmq.Context()
    server = context.socket(zmq.REP)
    server.bind(settings.MAILOFFLOADER_SOCKET)
    logger.info("server listening on socket: %s" % settings.MAILOFFLOADER_SOCKET)
    from newsletters.mail.helpers import send_mass_html_mail
    while True:
        msg = server.recv_json()
        server.send_string("ack") #ack before time-consuming execution
        logger.debug("received: %s" % (msg['subject'],))
        number_sent = send_mass_html_mail(msg['subject'], 
                                          msg['text_content'],
                                          msg['html_content'],
                                          msg['recipients'],
                                          int(msg['pk']),
                                          msg['from_email'],
                                          msg['test'],)

    sys.exit(0)

