from pytz import timezone as pytz_timezone
from datetime import timedelta, datetime

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

from ..enums import (
    SubscriptionStatus,
    BillingCycle,
    SubscriptionPlan,
    OrderVolume,
    PaymentProvider,
)
from applications.merchant.subscriptions.factory import (
    get_subscription_processor,
)
from conf.core.fields import DECIMAL_DEFAULTS
from conf.core.models import IdentityTimeBaseModel
from conf.core.enums import Currency, PaymentOption, PricingCurrency


class SubscriptionPricing(IdentityTimeBaseModel):
    """Subscriptions Model(Table) registers a user(customer )"""

    name = models.CharField(max_length=255)
    category = models.CharField(
        choices=SubscriptionPlan.choices(),
        max_length=50,
        default=SubscriptionPlan.default(),
    )
    intial_price = models.DecimalField(**DECIMAL_DEFAULTS)
    charge = models.DecimalField(**DECIMAL_DEFAULTS)
    service_charge = models.DecimalField(**DECIMAL_DEFAULTS)
    price_per_table = models.DecimalField(**DECIMAL_DEFAULTS)
    billing_price = models.DecimalField(**DECIMAL_DEFAULTS)
    billing_cycle = models.CharField(
        max_length=50,
        choices=BillingCycle.choices(),
        default=BillingCycle.default(),
    )
    order_volume = models.CharField(
        max_length=50,
        choices=OrderVolume.choices(),
        default=OrderVolume.default(),
    )
    percent_per_order = models.FloatField(default=0.00)
    currency = models.CharField(
        max_length=50, choices=PricingCurrency.choices(), default=PricingCurrency.default()
    )

    def save(self, *args, **kwargs):
        processor = get_subscription_processor(self.category)(self)
        self.service_charge = processor.get_running_cost(self.billing_cycle)
        self.billing_price = processor.calculate_billing_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class Subscription(IdentityTimeBaseModel):
    """Subscriptions Model(Table) registers a user(customer )"""

    # user = models.ForeignKey(
    #     to="accounts.User",
    #     related_name="subscriptions",
    #     on_delete=models.CASCADE,
    # )
    subscription_price = models.ForeignKey(
        to="SubscriptionPricing",
        related_name="subscriptions",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    restaurant = models.ForeignKey(
        to="merchant.Restaurant",
        related_name="subscriptions",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    server = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(
        choices=SubscriptionPlan.choices(),
        max_length=50,
        default=SubscriptionPlan.default(),
    )
    billing_cycle = models.CharField(
        max_length=50,
        choices=BillingCycle.choices(),
        default=BillingCycle.default(),
    )
    status = models.CharField(
        max_length=100,
        choices=SubscriptionStatus.choices(),
        default=SubscriptionStatus.default(),
    )
    payment_provider = models.CharField(
        max_length=50,
        choices=PaymentProvider.choices(),
        default=PaymentProvider.default(),
    )
    meta = models.JSONField(_("Meta"), default=dict, blank=True, null=True)

    billing_price = models.DecimalField(**DECIMAL_DEFAULTS)
    total_price = models.DecimalField(**DECIMAL_DEFAULTS)
    number_of_tables = models.PositiveSmallIntegerField(default=1)

    billing_count = models.PositiveSmallIntegerField(default=0)
    auto_renew = models.BooleanField(_("Auto Renew"), default=False)  # future
    contract_length = models.PositiveSmallIntegerField(
        default=1, help_text="In months/ years (30 days)"
    )
    current_payment = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        default=None,
    )
    next_payment = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        default=None,
    )

    date_cancelled = models.DateField(blank=True, null=True)
    contract_start_date = models.DateField(
        default=timezone.now,
        blank=True,
        null=True,
    )
    contract_end_date = models.DateField(blank=True, null=True)
    next_billing_date = models.DateTimeField(blank=True, null=True)
    currency = models.CharField(
        max_length=50, choices=Currency.choices(), default=Currency.default()
    )

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"

    def is_expired(self):
        return bool(datetime.today().date() > self.contract_end_date)

    def get_cycle_days(self) -> int:
        res = 30 if self.billing_cycle == BillingCycle.MONTHLY else 365
        if self.category == SubscriptionPlan.FREE:
            res = 7
        return res

    def update_contract_date(self):
        measure = self.get_cycle_days()
        duration = timedelta(days=self.contract_length * measure)
        self.contract_end_date = self.contract_start_date + duration

    def update_data_from_pricing(self):
        if self.category != self.subscription_price.category:
            self.category = self.subscription_price.category
        if self.billing_cycle != self.subscription_price.billing_cycle:
            self.billing_cycle = self.subscription_price.billing_cycle

    def update_meta_information(self, processor):
        if not self.meta:
            data = processor.construct_meta_data()
            self.meta = {"pricing": data}

    def save(self, *args, **kwargs):
        processor = get_subscription_processor(self.category)
        processor = processor(self.subscription_price, self)
        self.update_meta_information(processor)
        self.update_contract_date()
        self.total_price = processor.get_total()
        if self.is_expired():
            self.status = SubscriptionStatus.EXPIRED
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Subscription for {self.restaurant}"


class SubscriptionPayment(IdentityTimeBaseModel):
    """Subscriptions PaymentModel(Table)"""

    subscription = models.ForeignKey(
        to="Subscription",
        related_name="subscription_payments",
        on_delete=models.CASCADE,
    )
    payment_date = models.DateField(blank=True, null=True)
    amount = models.DecimalField(**DECIMAL_DEFAULTS)
    status = models.CharField(
        max_length=50,
        choices=PaymentOption.choices(),
        default=PaymentOption.default(),
    )
    expires_at = models.DateField(blank=True, null=True)
    currency = models.CharField(
        max_length=50, choices=Currency.choices(), default=Currency.default()
    )

    def is_expired(self):
        return bool(datetime.today().date() > self.expires_at)

    def __str__(self):
        return f"Payment for {self.subscription}"
