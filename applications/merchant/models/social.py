from django.db import models

from ..media import RestaurantMediaFolders
from services.cloud.aws.s3 import S3Resource
from conf.core.models import IdentityTimeBaseModel
from services.image_conversion.factory import get_image_service


class SocialAccount(IdentityTimeBaseModel):
    name = models.CharField(max_length=128)
    data_key = models.CharField(max_length=128, null=True, blank=True)
    data_value = models.CharField(max_length=128, null=True, blank=True)
    logo = models.FileField(
        upload_to=RestaurantMediaFolders.social_logo, null=True, blank=True
    )
    restaurantant = models.ForeignKey(
        "Restaurant",
        on_delete=models.CASCADE,
        related_name="social_accounts",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.name} social account"

    def save(self, *args, **kwargs):
        self.convert_to_png()
        super().save(*args, **kwargs)

    def convert_to_png(self):
        if self.logo and not self.logo.name.endswith(".png"):
            processor = get_image_service("png")
            self.site_favicon = processor.convert_model_image(
                self.site_favicon,
                model_field_name="FileField",
            )

    def delete(self, *args, **kwargs):
        s3_agent = S3Resource()
        s3_agent.delete_object(self.logo.name)
        super().delete(*args, **kwargs)
