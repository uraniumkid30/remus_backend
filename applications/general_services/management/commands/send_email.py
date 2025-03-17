from django.conf import settings
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string


from services.email_dispatcher import email_engine_factory
from applications.order.models import Order
from services.cloud.aws.utils import get_file_url


class Command(BaseCommand):
    help = "send africas talking sms"

    def handle(self, *args, **kwargs):
        order = Order.objects.filter().first()
        restaurant = order.table.restaurant
        logo_url = get_file_url(restaurant.logo.name)
        body1 = (
            "<p>hey just a test email <a href='' download='my_receipt'>Download</a></p>"
        )
        url = f"http://localhost:8000{order.get_admin_url()}"
        body2 = render_to_string(
            "order_email.html",
            {
                "table_name": "Table 1",
                "order_url": url,
                "logo_url": logo_url,
            },
        )
        attachments = [
            {
                "url": "https://test-490-django.s3.eu-central-1.amazonaws.com/files/pdf/receipts/order_payment/bobs.pdf",
                "name": "bobs.pdf",
            }
        ]
        data = {
            "body": body2,
            "subject": "test Mail",
            "sender_name": "bobby",
            "attachments": attachments,
        }
        to = [{"name": "chris okoro", "email": "christopherokoro007@gmail.com"}]
        _from = "uraniumkid30@gmail.com"
        cl = email_engine_factory("sentinel")
        cl.send_mail(to, _from, **data)
        self.stdout.write(self.style.SUCCESS("Email sent successfully"))
