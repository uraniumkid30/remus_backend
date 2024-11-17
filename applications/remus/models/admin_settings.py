from django.db import models

from conf.core.models import IdentityTimeBaseModel
from conf.core.fields import DECIMAL_DEFAULTS
from ..media import MediaFolders


class RemusSettings(IdentityTimeBaseModel):
    transaction_fee = models.DecimalField(**DECIMAL_DEFAULTS)
    logo = models.FileField(
        upload_to=MediaFolders.remus_logo, null=True, blank=True
    )
    logo_icon = models.FileField(
        upload_to=MediaFolders.remus_logo_icon, null=True, blank=True
    )
