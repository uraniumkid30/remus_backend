import uuid
from pytz import timezone as pytz_timezone
from datetime import timedelta, datetime

from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator

from conf.core.enums import PaymentStatus
from conf.core.models import IdentityTimeBaseModel, TempIdentityTimeBaseModel
from conf.core.fields import DECIMAL_DEFAULTS
from ..enums import OrderStatus, OrderMethod
from ..managers.sessions import SessionManager, ExpiredSessionManager
from applications.accounts.models import DeviceInfo
from applications.merchant.models import RestaurantPlatformSettings


def default_expiry_date():
    return datetime.now() + timedelta(minutes=30)


class Order(IdentityTimeBaseModel):
    customer = models.ForeignKey(
        "accounts.Customer",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="orders",
    )
    device = models.ForeignKey(
        "accounts.DeviceInfo",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="orders",
    )
    table = models.ForeignKey(
        "merchant.table",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="orders",
    )
    status = models.CharField(
        max_length=100,
        choices=OrderStatus.choices(),
        default=OrderStatus.default(),
    )
    total = models.DecimalField(**DECIMAL_DEFAULTS)
    total_wait_time = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
    )
    payment_status = models.CharField(
        max_length=50,
        choices=PaymentStatus.choices(),
        default=PaymentStatus.default(),
    )
    order_number = models.CharField(max_length=30, null=True, blank=True)
    order_note = models.CharField(max_length=100, null=True, blank=True)
    tax = models.DecimalField(**DECIMAL_DEFAULTS)

    def __str__(self):
        return f"{self.order_number} from {str(self.customer)} on table {self.table}"

    def generate_order_id(self):
        self.order_number = str(uuid.uuid4())[:10].upper()

    def get_admin_url(self):
        admin_order_url = f"admin:{self._meta.app_label}_"
        admin_order_url += f"{self._meta.model_name}_change"
        restaurant = self.table.restaurant
        platform = RestaurantPlatformSettings.objects.get(
            restaurant=restaurant,
        )
        path: str = reverse(
            admin_order_url,
            args=[self.id],
        )
        return f"{platform.api_domain}{path}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.generate_order_id()
        order_stat = [OrderStatus.SERVED, OrderStatus.CANCELLED]
        payment_stat = [PaymentStatus.SUCCESS]
        if self.status in order_stat and self.payment_status in payment_stat:
            try:
                dev = DeviceInfo.objects.get(id=self.device.id)
                dev.delete()
                self.device = None
            except Exception as err:
                print(err)
        super().save(*args, **kwargs)


class OrderItem(IdentityTimeBaseModel):
    order = models.ForeignKey(
        "Order",
        on_delete=models.CASCADE,
        related_name="order_items",
        null=True,
        blank=True,
    )
    product = models.ForeignKey(
        "product.Product", on_delete=models.CASCADE, related_name="order_items"
    )
    quantity = models.PositiveSmallIntegerField(default=1)
    price = models.DecimalField(**DECIMAL_DEFAULTS)
    discount = models.DecimalField(**DECIMAL_DEFAULTS)
    method = models.CharField(
        max_length=100,
        choices=OrderMethod.choices(),
        default=OrderMethod.default(),
    )

    def __str__(self):
        return f"{self.id}-{str(self.order)}"


class TableSession(TempIdentityTimeBaseModel):
    device = models.ForeignKey(
        "accounts.DeviceInfo",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="sessions",
    )
    table = models.ForeignKey(
        "merchant.table",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="sessions",
    )
    expires_at = models.DateTimeField(default=default_expiry_date)
    # objects = models.Manager()
    objects = SessionManager()
    expired_sessions = ExpiredSessionManager()

    def is_expired(self):
        tz = pytz_timezone("Africa/Lagos")
        now = tz.localize(datetime.now())
        return bool(now > self.expires_at)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
