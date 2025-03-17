import os
from django.conf import settings
from django.core.management.base import BaseCommand

from services.sms_dispatcher import sms_factory


class Command(BaseCommand):
    help = "send africas talking sms"
    def handle(self, *args, **kwargs):
        cl = sms_factory(destination_no="+2348168886668")
        cl.send_sms(**{
            "destination_phone_no": "+2348168886668",
            "text": "i sent this from Aff"
        })
        self.stdout.write(self.style.SUCCESS("SMS sent successful"))
