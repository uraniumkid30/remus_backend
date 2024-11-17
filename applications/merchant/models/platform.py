from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from ..media import MediaFolders
from conf.core.models import IdentityTimeBaseModel
import string


def _simple_domain_name_validator(value):
    """
    Validate that the given value contains no whitespaces to prevent common
    typos.
    """
    checks = ((s in value) for s in string.whitespace)
    if any(checks):
        raise ValidationError(
            _("The domain name cannot contain any spaces or tabs."),
            code="invalid",
        )


class MerchantPlatformSettings(IdentityTimeBaseModel):
    merchant = models.ForeignKey(
        "merchant.MerchantProfile",
        on_delete=models.CASCADE,
        related_name="platform_settings")
    domain = models.CharField(
        _("domain name"),
        max_length=100,
        validators=[_simple_domain_name_validator],
        unique=True,
    )
    name = models.CharField(_("display name"), max_length=50)
    site_title = models.CharField(max_length=64, blank=True, null=True)
    site_favicon = models.FileField(
        upload_to=MediaFolders.site_favicon, null=True, blank=True
    )

    class Meta:
        ordering = ["domain"]
        verbose_name_plural = "Merchant platform settings"

    def natural_key(self):
        return (self.domain,)

    def __str__(self):
        return f"{self.merchant} platform settings"
