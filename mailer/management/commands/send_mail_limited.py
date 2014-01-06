import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from mailer.engine import send_all


# allow a sysadmin to pause the sending of mail temporarily.
PAUSE_SEND = getattr(settings, "MAILER_PAUSE_SEND", False)


class Command(BaseCommand):
    args = "<limit> <throttle=0>"
    help = "Send a limited number of emails."
    
    def handle(self, *args, **options):
        logging.basicConfig(level=logging.DEBUG, format="%(message)s")
        logging.info("-" * 72)
        # if PAUSE_SEND is turned on don't do anything.
        limit = int(args[0])

        try:
            throttle = float(args[1])
        except IndexError:
            throttle = 0

        if not PAUSE_SEND:
            logging.info("Sending %d emails at" % limit)
            send_all(limit, throttle)
        else:
            logging.info("sending is paused, quitting.")
