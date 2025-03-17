from autoslug.fields import AutoSlugField
from django.db import models
from django.core.validators import MinValueValidator
from imagekit.models.fields import ImageSpecField
from pilkit.processors.resize import ResizeToFill

from ..media import MediaFolders
from conf.core.models import IdentityTimeBaseModel
from conf.core.fields import DECIMAL_NO_DEFAULT
from ..enums import ProductStatus


class Product(IdentityTimeBaseModel):
    sub_category = models.ForeignKey(
        "SubCategory", on_delete=models.CASCADE, related_name="products"
    )
    chef = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="products",
        blank=True,
        null=True,
    )
    ingredients = models.ManyToManyField(
        "Ingredient", related_name="products", null=True, blank=True
    )
    discount = models.ForeignKey(
        "Discount",
        verbose_name="Product Discount",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="products",
    )
    name = models.CharField(max_length=500)
    slug = AutoSlugField(populate_from="name", unique=True, null=True)
    description = models.TextField(blank=True, null=True)
    point = models.PositiveBigIntegerField(default=0)
    unit_price = models.DecimalField(**DECIMAL_NO_DEFAULT)
    wait_time = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
    )
    status = models.CharField(
        max_length=50,
        choices=ProductStatus.choices(),
        default=ProductStatus.default(),
    )
    image = models.ImageField(
        upload_to=MediaFolders.product_image_upload_to,
        blank=True,
        verbose_name="Product Image",
        null=True,
    )
    image_thumbnail = ImageSpecField(
        source="image",
        processors=[ResizeToFill(100, 100)],
        format="JPEG",
        options={"quality": 80},
    )
    image_thumbnail.short_description = "Thumbnail"

    def final_price(self):
        price = self.unit_price
        discount = (
            self.discount.percent
            if (self.discount and self.discount.is_valid and self.discount.is_active)
            else 0
        )
        final = price if not discount else (price * (100 - discount)) / 100
        return final

    final_price.short_description = "Final Price"

    def __str__(self):
        return self.name


class ProductStock(IdentityTimeBaseModel):
    product = models.OneToOneField(
        "Product",
        on_delete=models.CASCADE,
        related_name="product_stocks",
        null=True,
        blank=True,
    )
    quantity = models.PositiveSmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        if not self.quantity > 0:
            self.product.status = ProductStatus.AVAILABLE
        else:
            self.product.status = ProductStatus.UNAVAILABLE
        self.product.save()
        super().save(*args, **kwargs)
