from datetime import datetime

from autoslug.fields import AutoSlugField
from django.db import models
from pytz import timezone as pytz_timezone
from django.core.validators import MinValueValidator, MaxValueValidator

from conf.core.models import IdentityTimeBaseModel


class Coupon(IdentityTimeBaseModel):
    restaurant = models.ForeignKey(
        "merchant.Restaurant",
        on_delete=models.CASCADE,
        related_name="coupons",
        blank=True, null=True
    )
    name = models.CharField(
        max_length=500, unique=True
    )
    slug = AutoSlugField(populate_from="name", unique=True, null=True)
    description = models.CharField(
        max_length=500, blank=True, null=True
    )
    code = models.CharField("Coupon Code", max_length=50, unique=True)
    percent = models.PositiveSmallIntegerField(
        "Coupon Percentage",
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    is_active = models.BooleanField(default=False)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def is_valid(self):
        now = datetime.now()
        return bool(now < self.valid_to)

    is_valid.boolean = True
    is_valid.short_description = "Valid"

    def period(self):
        delta = self.valid_to - self.valid_from
        result = self.days_hours_minutes(delta)
        return f"{result[0]} Days - {result[1]} Hours - {result[2]} Minutes"

    period.short_description = "Period"

    def days_hours_minutes(self, td):
        return td.days, td.seconds // 3600, (td.seconds // 60) % 60

    def remaining_time(self):
        tz = pytz_timezone('Africa/Lagos')
        now = tz.localize(datetime.now())
        delta = self.valid_to - now
        result = self.days_hours_minutes(delta)
        return f"{result[0]} Days - {result[1]} Hours - {result[2]} Minutes"

    remaining_time.short_description = "Remaining Time"

    def __str__(self):
        return self.name
