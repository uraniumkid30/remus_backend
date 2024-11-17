from django.db import models

from ..enums import QRScanResult
from conf.core.models import IdentityTimeBaseModel


class QRScan(IdentityTimeBaseModel):
    qr = models.ForeignKey(
        "merchant.QRTag", on_delete=models.CASCADE, related_name="scan_log"
    )
    receipt_id = models.UUIDField(null=True, blank=True, editable=False)
    result = models.CharField(
        choices=QRScanResult.choices(),
        default=QRScanResult.default(),
        max_length=32
    )
    user_agent = models.CharField(null=True, blank=True, max_length=256)
    source = models.CharField(null=True, blank=True, max_length=32)
