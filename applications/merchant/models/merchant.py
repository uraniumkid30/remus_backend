from django.db import models

from ..media import MerchantMediaFolders
from services.cloud.aws.s3 import S3Resource
from conf.core.models import IdentityTimeBaseModel
from services.image_conversion.factory import get_image_service


def default_img():
    return "default_images/restaurant_logo_main.png"


class MerchantProfile(IdentityTimeBaseModel):
    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="merchants"
    )
    name = models.CharField(max_length=256)
    display_name = models.CharField(max_length=32)
    tax_id = models.CharField(max_length=32, null=True, blank=True)
    vat_id = models.CharField(max_length=32, null=True, blank=True)
    logo = models.FileField(
        upload_to=MerchantMediaFolders.logo,
        null=True,
        blank=True,
        default=default_img,
    )

    def __str__(self):
        return self.name

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

    def delete(self, *args, **kwargs):
        s3_agent = S3Resource()
        s3_agent.delete_object(self.logo.name)
        super().delete(*args, **kwargs)
