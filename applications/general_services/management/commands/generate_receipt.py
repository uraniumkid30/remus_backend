import os
import pathlib
from django.conf import settings
from django.core.management.base import BaseCommand
from services.cloud.aws.s3 import S3Resource

from services.receipts.order_payment import OrderReceiptPDF
from services.receipts.enums import (
    PaymentReceiptParams,
    OrderItems,
    OrderTotal,
    Payment,
    RestaurantData,
)
from applications.merchant.models import MerchantProfile


class Command(BaseCommand):
    help = "send africas talking sms"

    def handle(self, *args, **kwargs):
        payment = Payment(
            "card",
            "33,000",
            "Successful",
            "p34n5jj5nng",
            "23/12/2024",
            "14:38:34",
        )
        items = [
            OrderItems(*["Carossi Red Wine", "1", "10,000", "10,000"]),
            OrderItems(*["Fried Rice", "2", "11,000", "22,000"]),
            OrderItems(*["Plantain", "1", "1,000", "1,000"]),
        ]
        total = OrderTotal(
            "33,000",
            "0.00",
            "0.00",
            "33,000",
            "4",
        )
        #cc = RunningCost.objects.get(name="aws")
        cc = MerchantProfile.objects.get(name="Ile Iyan")
        fname = cc.receipt_thumbnail.name.split("/")[-1]
        self.download_file(fname, cc.receipt_thumbnail.name)
        restaurant = RestaurantData(
            os.path.join(settings.ARCHIVE_DIR, fname),
            "ILE IYAN",
            "30 oluwole street akoka yaba lagos",
        )
        note = "Thank You for Dinning With Us! See you again."
        barcode = "5901234123457"
        order_id = "56u85h8h85"
        receipt_id = "b4u5ukk3k3k"
        data = PaymentReceiptParams(
            restaurant,
            items,
            total,
            payment,
            note,
            barcode,
            "generated_barcode",
            os.path.join(settings.ARCHIVE_DIR, "generated_barcode"),
            order_id,
            receipt_id,
            "₦",
        )
        r_name = os.path.join(settings.ARCHIVE_DIR, "test_receipt.pdf")
        OrderReceiptPDF.build_pdf(r_name, settings.PDF_FONTS_DIR, data)
        self.delete_files(os.path.join(settings.ARCHIVE_DIR, fname))
        self.delete_files(os.path.join(settings.ARCHIVE_DIR, "generated_barcode.png"))
        self.stdout.write(self.style.SUCCESS("Receipt Generated successfully"))

    def download_file(self, filename, fpath):
        path_to_file = os.path.join(settings.ARCHIVE_DIR, filename)
        s3_agent = S3Resource()
        s3_agent.download_file(
            path_to_file, f"media/{fpath}"
        )

    def delete_files(self, file_path):
        file_to_rem = pathlib.Path(file_path)
        file_to_rem.unlink()
