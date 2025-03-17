import os
from typing import Union, NoReturn

from autoslug.fields import AutoSlugField
from django.db import models
from django.conf import settings
from django.core.files.storage import DefaultStorage

from ..media import RestaurantMediaFolders
from ..enums import QRType, DaysOfTheWeek
from services.cloud.aws.s3 import S3Resource
from conf.core.models import IdentityTimeBaseModel
from services.image_conversion.factory import get_image_service


def default_img():
    return "default_images/restaurant_logo_main.png"


class Restaurant(IdentityTimeBaseModel):
    merchant = models.ForeignKey(
        "MerchantProfile", on_delete=models.CASCADE, related_name="restaurants"
    )
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True, null=True)
    restaurant_id = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        help_text="Restaurant ID used by the merchant",
    )
    name = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        help_text="Restaurant name used by the merchant",
    )
    slug = AutoSlugField(
        populate_from="name", unique=True,
    )
    logo = models.FileField(
        upload_to=RestaurantMediaFolders.logo,
        blank=True,
        default=default_img,
    )
    logo_inside_qr_code = models.FileField(
        upload_to=RestaurantMediaFolders.logo_inside_qr_code,
        blank=True,
        default=default_img,
    )
    background = models.FileField(
        upload_to=RestaurantMediaFolders.background,
        blank=True,
        default=default_img,
    )
    receipt_thumbnail = models.FileField(
        upload_to=RestaurantMediaFolders.receipt_thumbnail,
        null=True,
        blank=True,
    )
    short_note = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        default="Thank you for Dinning with us",
    )

    def __str__(self):
        return f"{self.merchant.name}"

    def save(self, *args, **kwargs):
        self.convert_to_png()
        self.convert_to_circular_thumbnail()
        super().save(*args, **kwargs)

    def convert_to_png(self):
        if self.logo and not self.logo.name.endswith(".png"):
            processor = get_image_service("png")
            self.logo = processor.convert_model_image(
                self.logo,
                model_field_name="FileField",
            )
        if self.logo_inside_qr_code and not self.logo_inside_qr_code.name.endswith(
            ".png"
        ):
            processor = get_image_service("png")
            self.logo_inside_qr_code = processor.convert_model_image(
                self.logo_inside_qr_code,
                model_field_name="FileField",
            )
        if self.background and not self.background.name.endswith(".png"):
            processor = get_image_service("png")
            self.background = processor.convert_model_image(
                self.background,
                model_field_name="FileField",
            )

    def convert_to_circular_thumbnail(self):
        if self.logo and not self.receipt_thumbnail:
            processor = get_image_service("png")
            self.receipt_thumbnail = processor.create_circular_thumbnail(
                self.logo,
                model_field_name="FileField",
            )

    def delete(self, *args, **kwargs):
        s3_agent = S3Resource()
        s3_agent.delete_object(self.logo.name)
        s3_agent.delete_object(self.logo_inside_qr_code.name)
        s3_agent.delete_object(self.background.name)
        s3_agent.delete_object(self.receipt_thumbnail.name)
        super().delete(*args, **kwargs)


class OperationSchedule(IdentityTimeBaseModel):
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    day = models.CharField(
        max_length=50,
        choices=DaysOfTheWeek.choices(),
        default=DaysOfTheWeek.default(),
    )
    restaurant = models.ForeignKey(
        "Restaurant",
        on_delete=models.CASCADE,
        related_name="operation_schedules",
    )


class Table(IdentityTimeBaseModel):
    restaurant = models.ForeignKey(
        "Restaurant", on_delete=models.CASCADE, related_name="tables"
    )
    name = models.CharField(max_length=500, unique=True)
    slug = AutoSlugField(populate_from="name", unique=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name


qr_storage = DefaultStorage()

if not settings.DEBUG:
    from conf.storage_backends import MediaAttachmentStorage

    qr_storage = MediaAttachmentStorage()


class QRTag(IdentityTimeBaseModel):
    table = models.ForeignKey(
        "Table",
        on_delete=models.CASCADE,
        related_name="qr_links",
    )
    position = models.CharField(max_length=64, blank=True, null=True)
    type = models.CharField(
        max_length=30, choices=QRType.choices(), default=QRType.default()
    )
    background_color = models.CharField(max_length=10, default="#FFFFFF")
    fill_color = models.CharField(max_length=10, default="#000000")
    qr_image = models.FileField(
        upload_to=RestaurantMediaFolders.qr_codes,
        editable=False,
        null=True,
        storage=qr_storage,
    )
    domain = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        editable=False,
    )

    def is_available(self):
        return self.point_of_sale is None

    def get_pos_provider(self):
        return self.point_of_sale.provider

    def get_absolute_url(self):
        from django.urls import reverse

        url_name: str = "customer_applications:merchant:qr_request_menu"
        return reverse(url_name, args=[str(self.id)])

    def get_restaurant_api_domain(self):
        from applications.merchant.utils.urls import get_restaurant_api_domain

        if self.domain:
            return self.domain
        try:
            restaurant = self.table.restaurant
        except Exception:
            return ""
        else:
            return get_restaurant_api_domain(restaurant)

    def get_restaurant_qr_logo(self) -> Union[str, None]:
        """Returns the name of the logo and the root location of the file"""
        try:
            result = ""
            restaurant = self.table.restaurant
            logo = restaurant.logo_inside_qr_code
            if logo:
                result = logo.name
        except Exception as err:
            print(f"error {err}")
        finally:
            return result

    def _create_qr_image(self) -> NoReturn:
        from services.qr_code import QRCodeGenerator
        from services.qr_code.engines.factory import (
            get_qr_processor,
            AbstractQRCodeEngine,
        )

        logo_id: str = self.get_restaurant_qr_logo()
        base_url: str = self.get_restaurant_api_domain()

        # data: str = f"https://{base_url}{self.table.id}"  # here
        data: str = os.path.join(base_url, self.get_absolute_url()[1:])
        file_name: str = f"qr-{self.id}.png"
        configuration: dict = {
            "image_name": file_name,
            "logo_name": logo_id if logo_id else "",
            "save_dir": RestaurantMediaFolders.qr_codes,
        }
        qr_code_engine: AbstractQRCodeEngine = get_qr_processor(
            self.type, configuration
        )
        qr_code = QRCodeGenerator.generate_qr_code(
            data=data, qr_code_engine=qr_code_engine
        )
        if qr_code:
            saved_qr_code = QRCodeGenerator.save_qr_code(qr_code, file_name)
            self.qr_image = saved_qr_code

    def save(self, *args, **kwargs):
        if not self.qr_image:
            self._create_qr_image()
            self.domain = self.get_restaurant_api_domain()
        super().save(*args, **kwargs)

    def __str__(self):
        created_at_str = self.created_at.strftime("%Y-%m-%d %H:%M")
        default: str = f" at Position: {self.position}"
        qr_position = "" if self.position is None else default
        id_str = str(self.id)
        display_id = f"{id_str[:4]}...{id_str[-4:]}"
        result = f"QRTag {display_id} created at {created_at_str}. "
        result += f"Placed at {self.table}{qr_position}"
        return result

    def delete(self, *args, **kwargs):
        s3_agent = S3Resource()
        s3_agent.delete_object(self.qr_image.name)
        super().delete(*args, **kwargs)
