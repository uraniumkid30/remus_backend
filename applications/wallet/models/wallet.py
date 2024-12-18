from decimal import Decimal

from django.db import models
from conf.core.models import IdentityTimeBaseModel
from conf.core.fields import DECIMAL_DEFAULTS
from ..enums import (
    WithdrawalStatusType,
    WalletStatus,
    CategoryType,
    TransactionDirection

)


class Wallet(IdentityTimeBaseModel):
    user = models.OneToOneField(
        to="accounts.User", on_delete=models.CASCADE,
        related_name="wallets"
    )
    amount = models.DecimalField(**DECIMAL_DEFAULTS)
    bonus_balance = models.DecimalField(**DECIMAL_DEFAULTS)
    status = models.CharField(
        max_length=50,
        choices=WalletStatus.choices(),
        default=WalletStatus.default()
    )
    overdraft_limit = models.DecimalField(**DECIMAL_DEFAULTS)
    overdraft = models.DecimalField(**DECIMAL_DEFAULTS)
    allow_overdraft = models.BooleanField(default=False)

    def __str__(self):
        return "{}'s Wallet".format(self.user)

    def is_balance_sufficient(self, amount):
        if self.balance > Decimal(amount) or self.balance == Decimal(amount):
            return True
        return False

    def allow_bonus_and_balance_aggregation(self, amount):
        if self.balance == Decimal("0.00"):
            return False
        return True

    @property
    def wallet_balance(self):
        """ Return the wallet balance """
        return self.amount

    def can_take_overdraft(self, new_overdraft):
        """ Method checks if further overdraft can be allowed """
        overdraft_amount = int(self.overdraft_limit) - int(new_overdraft)
        if int(overdraft_amount) > int(self.overdraft_limit):
            return False
        return True

    @property
    def operator_name(self):
        return self.operator.name

    @classmethod
    def take_overdraft(cls, overdraft):
        cls.overdraft_limit - overdraft
        cls.overdraft + overdraft
        cls.save


class WalletHistory(IdentityTimeBaseModel):
    wallet = models.ForeignKey(
        to="Wallet", on_delete=models.DO_NOTHING,
        related_name="wallet_histories"
    )
    description = models.CharField(max_length=300, default='')
    transaction_category = models.CharField(
        max_length=20, choices=CategoryType.choices(),
        default=CategoryType.default()
    )
    transaction_type = models.CharField(
        max_length=20, choices=TransactionDirection.choices(),
        default=TransactionDirection.default()
    )
    previous_balance = models.DecimalField(**DECIMAL_DEFAULTS)
    new_balance = models.DecimalField(**DECIMAL_DEFAULTS)
    main_balance = models.DecimalField(**DECIMAL_DEFAULTS)
    bonus_balance = models.DecimalField(**DECIMAL_DEFAULTS)

    def __str__(self):
        return "{}'s wallet history".format(self.wallet)

    @property
    def withdrawal_amount(self):
        amount = abs(self.previous_balance - self.new_balance)
        return amount

    def transaction_amount(self):
        amount = abs(self.previous_balance - self.new_balance)
        return amount

    class Meta:
        ordering = ["-created_at"]
        verbose_name = 'history'
        verbose_name_plural = 'histories'


class TransactionRecord(IdentityTimeBaseModel):
    reference = models.CharField(max_length=200, blank=False, null=False)
    amount = models.DecimalField(**DECIMAL_DEFAULTS)
    transaction_date = models.DateTimeField(blank=True, null=True)
    receiver = models.CharField(max_length=250)
    sender = models.CharField(max_length=250)
    customer = models.ManyToManyField(
        to="finance.BankDetail",
        related_name="transaction_records",
        blank=True, null=True
    )

    def __str__(self):
        return "Transaction record{}".format(self.reference)


class MoneyRequest(IdentityTimeBaseModel):
    user = models.ForeignKey(
        to="accounts.User", on_delete=models.DO_NOTHING,
        related_name="money_requests"
    )
    request_type = models.CharField(
        max_length=20, choices=WithdrawalStatusType.choices(),
        default=WithdrawalStatusType.default()
    )
    status = models.CharField(
        max_length=20, choices=WithdrawalStatusType.choices(),
        default=WithdrawalStatusType.default()
    )
    recipient_code = models.CharField(
        max_length=255, default=""
    )
    amount_requested = models.DecimalField(**DECIMAL_DEFAULTS)
    amount_paid = models.DecimalField(**DECIMAL_DEFAULTS)
    fee = models.DecimalField(**DECIMAL_DEFAULTS)

    def __str__(self):
        return f"{self.request_type} Request by {self.user}"

    class Meta:
        ordering = ["-created_at"]
