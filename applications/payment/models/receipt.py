import os
import pathlib
from io import BytesIO

from django.core.files.base import ContentFile
from django.db import models
from django.urls import reverse
from django.conf import settings

from conf.core.models import IdentityTimeBaseModel
from ..media import MediaFolders
from conf.core.enums import Currency
from services.identifier import get_id_generator
from services.cloud.aws.s3 import S3Resource
from services.receipts.order_payment import OrderReceiptPDF
from services.receipts.enums import (
    PaymentReceiptParams,
    OrderItems,
    OrderTotal,
    Payment,
    RestaurantData,
)
from applications.order.utils import get_order_items_summary


class Receipt(IdentityTimeBaseModel):
    payment = models.OneToOneField(
        "Payment",
        on_delete=models.CASCADE,
        related_name="receipt",
        blank=True,
        null=True,
    )
    receipt_id = models.CharField(max_length=10, blank=True, null=True)
    data = models.JSONField(default=dict, blank=True, null=True)
    pdf_document = models.FileField(
        upload_to=MediaFolders.receipt_file, null=True, blank=True
    )

    def get_absolute_url(self):
        return reverse("receipt", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.receipt_id}"

    def save(self, *args, **kwargs):
        if not self.receipt_id:
            id_generator = get_id_generator("randomstring")
            self.receipt_id = id_generator.generate_id("R", 10)
        if not self.pdf_document:
            self.pdf_document, self.data = self.create_receipt()
        super().save(*args, **kwargs)

    def create_receipt(self):
        receipt_name: str = self.receipt_id
        currency = Currency.get_symbol(self.payment.currency)
        restaurant_record = self.payment.order.table.restaurant
        payment = Payment(
            method=self.payment.payment_method,
            amount=str(self.payment.amount_paid),
            status=self.payment.status,
            id=self.payment.payment_id,
            date=str(self.payment.created_at.date()),
            time=str(self.payment.created_at.time()),
        )
        items_sumamry = get_order_items_summary(self.payment.order)
        items = []
        for item in items_sumamry["items"]:
            items.append(
                OrderItems(
                    item["name"],
                    str(item["quantity"]),
                    str(item["unit_price"]),
                    str(item["amount"]),
                )
            )
        total = OrderTotal(
            str(items_sumamry["total"]),
            str(self.payment.order.tax),
            str(items_sumamry["total"]),
            str(self.payment.order.total),
            str(len(items_sumamry["items"])),
        )
        logo_path = restaurant_record.receipt_thumbnail.name
        logo_name = logo_path.split("/")[-1]
        self.download_file(logo_name, logo_path)

        restaurant = RestaurantData(
            os.path.join(settings.ARCHIVE_DIR, logo_name),
            restaurant_record.name,
            restaurant_record.address.name,
        )
        note = restaurant_record.short_note
        order_id = self.payment.order.order_number
        receipt_id = receipt_name
        data = PaymentReceiptParams(
            restaurant,
            items,
            total,
            payment,
            note,
            self.payment.barcode,
            self.payment.barcode,
            os.path.join(settings.ARCHIVE_DIR, self.payment.barcode),
            order_id,
            receipt_id,
            currency,
        )

        buffer = BytesIO()
        OrderReceiptPDF.build_pdf(buffer, settings.PDF_FONTS_DIR, data)
        self.delete_files(os.path.join(settings.ARCHIVE_DIR, logo_name))
        self.delete_files(
            os.path.join(settings.ARCHIVE_DIR, f"{self.payment.barcode}.png")
        )
        buffer.seek(0)
        pdf = buffer.getvalue()
        file_data = ContentFile(pdf)
        file_data.name = f"{receipt_name}.pdf"
        return file_data, data.to_dict()

    def download_file(self, filename, fpath):
        path_to_file = os.path.join(settings.ARCHIVE_DIR, filename)
        s3_agent = S3Resource()
        s3_agent.download_file(path_to_file, f"media/{fpath}")

    def delete_files(self, file_path):
        file_to_rem = pathlib.Path(file_path)
        file_to_rem.unlink()

    def delete(self, *args, **kwargs):
        s3_agent = S3Resource()
        s3_agent.delete_object(self.pdf_document.name)
        super().delete(*args, **kwargs)
