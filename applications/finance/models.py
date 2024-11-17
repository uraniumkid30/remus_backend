from django.db import models

from conf.core.models import IdentityTimeBaseModel
from .enums import (
    Source,
    AccountType
)


class BankDetail(IdentityTimeBaseModel):
    user = models.ForeignKey(
        to="accounts.User",
        on_delete=models.CASCADE,
        related_name="bank_details"
    )
    type = models.CharField(
        max_length=50, choices=AccountType.choices(),
        default=AccountType.default()
    )
    source = models.CharField(
        max_length=50, choices=Source.choices(), default=Source.default()
    )
    account_name = models.CharField(max_length=250)
    account_number = models.CharField(max_length=20, unique=True)
    bank_name = models.CharField(max_length=100)
    bank_code = models.CharField(max_length=100)
    bvn = models.CharField(max_length=20, blank=True, null=True)
    card_number = models.CharField(max_length=30, blank=True, null=True)
    recipient_code = models.CharField(max_length=100, blank=True, null=True)
    account_reference = models.CharField(max_length=100, blank=True, null=True)
    reservation_reference = models.CharField(
        max_length=250, blank=True, null=True
    )
    default = models.BooleanField(default=False)

    @property
    def phone_no(self):
        return self.user.phone_no

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    def __str__(self):
        return '{}'.format(self.user)
