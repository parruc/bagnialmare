# -*- coding: utf-8 -*-
from django.db.models import signals
from authauth.models import Manager
from authauth.signals import mail_for_manager
from bagni.models import Bagno
from bagni.signals import mail_for_bagno
from booking.models import Booking
from booking.signals import mail_for_booking

signals.post_save.connect(mail_for_manager, sender=Manager)
signals.post_save.connect(mail_for_bagno, sender=Bagno)

signals.post_save.connect(mail_for_booking, sender=Booking)
