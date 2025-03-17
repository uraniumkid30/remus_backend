from django.db import models

from ..enums import (
    PaymentProvider,
)
from conf.core.models import IdentityTimeBaseModel
from conf.core.enums import Currency
from .subscription import Subscription
from applications.payment.integrations.services.factory import get_service
from applications.merchant.utils.banks import BANK_CHOICES, get_bank_code


class BankDetail(IdentityTimeBaseModel):
    restaurant = models.OneToOneField(
        to="merchant.Restaurant",
        related_name="bank_detail",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    account_name = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    account_id = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    account_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )
    bank_name = models.CharField(max_length=250, choices=BANK_CHOICES, default=None)
    bank_code = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    payment_provider = models.CharField(
        max_length=50,
        choices=PaymentProvider.choices(),
        default=PaymentProvider.default(),
    )
    recipient_code = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    currency = models.CharField(
        max_length=5, choices=Currency.choices(), default=Currency.default()
    )

    def __str__(self):
        return "Bank details for {}.".format(self.restaurant)

    def save(self, *args, **kwargs):
        if not self.bank_code and self.bank_name:
            self.bank_code = get_bank_code(self.bank_name)
        if not self.account_id and self.account_number and self.bank_code:
            self.account_id = self.create_account_id()
        super().save(*args, **kwargs)

    def create_account_id(
        self,
    ):
        sub = Subscription.objects.get(restaurant=self.restaurant)
        data = {
            "account_name": self.account_name,
            "bank_code": self.bank_code,
            "account_number": self.account_number,
            "restaurant_name": self.restaurant.name,
        }
        service = get_service(self.payment_provider)
        return service.create_account_id(sub, data)
