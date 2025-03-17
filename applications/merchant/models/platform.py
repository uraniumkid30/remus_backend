import string

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from ..media import RestaurantMediaFolders
from services.cloud.aws.s3 import S3Resource
from conf.core.models import IdentityTimeBaseModel
from services.image_conversion.factory import get_image_service


def _simple_domain_name_validator(value):
    """
    Validate that the given value contains no whitespaces to prevent common
    typos.
    """
    if value:
        checks = ((s in value) for s in string.whitespace)
        if any(checks):
            raise ValidationError(
                _("The domain name cannot contain any spaces or tabs."),
                code="invalid",
            )


class RestaurantPlatformSettings(IdentityTimeBaseModel):
    restaurant = models.OneToOneField(
        "merchant.Restaurant",
        on_delete=models.CASCADE,
        related_name="platform_setting",
    )
    site_favicon = models.FileField(
        upload_to=RestaurantMediaFolders.site_favicon, null=True, blank=True
    )
    api_domain = models.CharField(
        max_length=100,
        validators=[_simple_domain_name_validator],
        unique=True,
        default=None
    )
    domain_name = models.CharField(max_length=250, blank=True, null=True)
    site_title = models.CharField(max_length=64, blank=True, null=True)
    website = models.URLField(null=True, blank=True)
    custom_link = models.CharField(max_length=350, null=True, blank=True)

    class Meta:
        ordering = ["api_domain"]
        verbose_name_plural = "Restaurant platform setting"

    def natural_key(self):
        return (self.api_domain,)

    def __str__(self):
        return f"{self.restaurant} platform setting"

    def save(self, *args, **kwargs):
        self.convert_to_png()
        super().save(*args, **kwargs)

    def convert_to_png(self):
        if self.site_favicon and not self.site_favicon.name.endswith(".png"):
            processor = get_image_service("png")
            self.site_favicon = processor.convert_model_image(
                self.site_favicon,
                model_field_name="FileField",
            )

    def delete(self, *args, **kwargs):
        s3_agent = S3Resource()
        s3_agent.delete_object(self.site_favicon.name)
        super().delete(*args, **kwargs)
