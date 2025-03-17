from datetime import timedelta

from django.db import models

from ..media import MediaFolders
from conf.core.models import IdentityTimeBaseModel
from conf.core.fields import DECIMAL_DEFAULTS
from services.cloud.aws.s3 import S3Resource
from conf.core.enums import CustomEnum, Currency, PaymentOption


class Interval(CustomEnum):
    YEARLY = "yearly"
    MONTHLY = "monthly"
    ONE_TIME = "one_time"

    @classmethod
    def choices(cls):
        return (
            (cls.YEARLY, "Yearly"),
            (cls.MONTHLY, "Monthly"),
            (cls.ONE_TIME, "One_Time"),
        )

    @classmethod
    def default(cls):
        return cls.MONTHLY


class AdministratorSettings(IdentityTimeBaseModel):
    transaction_fee = models.DecimalField(**DECIMAL_DEFAULTS)
    logo = models.FileField(
        upload_to=MediaFolders.administrator_logo, null=True, blank=True
    )
    logo_icon = models.FileField(
        upload_to=MediaFolders.administrator_logo_icon, null=True, blank=True
    )

    def delete(self, *args, **kwargs):
        s3_agent = S3Resource()
        s3_agent.delete_object(self.logo.name)
        s3_agent.delete_object(self.logo_icon.name)
        super().delete(*args, **kwargs)


class RunningCost(IdentityTimeBaseModel):
    name = models.CharField(max_length=100)
    currency = models.CharField(
        max_length=50, choices=Currency.choices(), default=Currency.default()
    )
    fee = models.DecimalField(**DECIMAL_DEFAULTS)
    interval = models.CharField(
        max_length=50,
        choices=Interval.choices(),
        default=Interval.default(),
    )
    status = models.CharField(
        max_length=50,
        choices=PaymentOption.choices(),
        default=PaymentOption.default(),
    )
    annual_fee = models.DecimalField(**DECIMAL_DEFAULTS)
    monthly_fee = models.DecimalField(**DECIMAL_DEFAULTS)
    last_payment_date = models.DateTimeField(blank=True, null=True)
    next_payment_date = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.interval == Interval.MONTHLY:
            self.annual_fee = self.fee * 12
            self.monthly_fee = self.fee
        elif self.interval == Interval.YEARLY:
            self.annual_fee = self.fee
            self.monthly_fee = self.fee / 12
        duration = 30 if self.interval == Interval.MONTHLY else 365
        if self.last_payment_date:
            self.next_payment_date = self.last_payment_date + timedelta(days=duration)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Service cost for {self.name}"
