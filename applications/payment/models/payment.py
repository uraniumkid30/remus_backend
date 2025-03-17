from django.db import models
from django.urls import reverse

from conf.core.models import IdentityTimeBaseModel
from conf.core.fields import DECIMAL_DEFAULTS
from conf.core.enums import Currency, PaymentStatus
from ..enums import PaymentMethod
from services.identifier import get_id_generator


class Payment(IdentityTimeBaseModel):
    order = models.OneToOneField("order.Order", on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=20, null=True, blank=True)
    payment_method = models.CharField(
        max_length=50,
        choices=PaymentMethod.choices(),
        default=PaymentMethod.default(),
    )
    barcode = models.CharField(max_length=20, null=True, blank=True)
    amount = models.DecimalField(**DECIMAL_DEFAULTS)
    amount_paid = models.DecimalField(**DECIMAL_DEFAULTS)
    merchant_amount = models.DecimalField(**DECIMAL_DEFAULTS)
    operator_amount = models.DecimalField(**DECIMAL_DEFAULTS)
    status = models.CharField(
        max_length=50,
        choices=PaymentStatus.choices(),
        default=PaymentStatus.default(),
    )
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices(),
        default=Currency.default(),
    )
    payment_method_meta = models.JSONField(default=dict, blank=True, null=True)

    def get_absolute_url(self):
        return reverse("receipt", kwargs={"pk": self.pk})

    def __str__(self):
        return (
            f"{self.payment_id} - {self.payment_method} - {self.amount} {self.currency}"
        )

    def save(self, *args, **kwargs):
        id_generator = get_id_generator("randomstring")
        if not self.payment_id:
            self.payment_id = id_generator.generate_id("OP", 6)
        if not self.barcode:
            self.barcode = id_generator.generate_id("", 13, "", "numbers")
        if not self.amount:
            self.amount = self.order.total
        super().save(*args, **kwargs)
