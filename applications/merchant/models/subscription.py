from datetime import datetime

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

from ..enums import (
    SubscriptionStatus,
    BillingCycle,
    SubscriptionType,
    CategoryType,
    CategoryPrice,
)
from conf.core.models import IdentityTimeBaseModel


class Subscription(IdentityTimeBaseModel):
    """Subscriptions Model(Table) registers a user(customer )
    """
    user = models.ForeignKey(
        to="accounts.User",
        related_name="subscriptions",
        on_delete=models.CASCADE,
    )
    server = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    app_type = models.CharField(
        max_length=70,
        choices=SubscriptionType.choices(),
        default=SubscriptionType.default()
        )
    category = models.CharField(
        choices=CategoryType.choices(), max_length=50,
        default=CategoryType.BASIC
    )
    category_price = models.IntegerField(
        choices=CategoryPrice.choices(), default=CategoryPrice.default()
    )
    price = models.CharField(max_length=255, blank=True, null=True)
    billing_cycle = models.SmallIntegerField(
        choices=BillingCycle.choices(), default=BillingCycle.MONTHLY
    )
    status = models.CharField(
        _("Status"), max_length=100,
        choices=SubscriptionStatus.choices(),
        default=SubscriptionStatus.default()
    )
    contract_length = models.IntegerField(blank=True, null=True)  # days
    meta = models.JSONField(_("Meta"), default=dict, blank=True, null=True)

    auto_renew = models.BooleanField(_("Auto Renew"), default=False)
    fixed_contract = models.BooleanField(default=False, null=True)

    created = models.DateField(default=timezone.now, blank=True, null=True)
    date_cancelled = models.DateField(blank=True, null=True)
    contract_start_date = models.DateField(
        default=timezone.now, blank=True, null=True
    )
    contract_end_date = models.DateField(blank=True, null=True)
    billing_cycle_updated = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
