from autoslug.fields import AutoSlugField
from django.db import models
from imagekit.models.fields import ImageSpecField
from pilkit.processors.resize import ResizeToFill

from ..media import MediaFolders
from conf.core.models import IdentityTimeBaseModel


class Category(IdentityTimeBaseModel):
    restaurant = models.ForeignKey(
        "merchant.Restaurant",
        on_delete=models.CASCADE,
        related_name="categories",
        blank=True, null=True
    )
    name = models.CharField(
        max_length=500, unique=True
    )
    slug = AutoSlugField(populate_from="name", unique=True, null=True)
    description = models.CharField(
        max_length=500, blank=True, null=True
    )
    is_visible = models.BooleanField(default=True)
    image = models.ImageField(
        upload_to=MediaFolders.product_category_image_upload_to,
        blank=True, verbose_name="Product Category Image",
        null=True,
    )
    image_thumbnail = ImageSpecField(
        source="image",
        processors=[ResizeToFill(100, 100)],
        format="JPEG",
        options={"quality": 80}
    )
    image_thumbnail.short_description = "Thumbnail"

    def __str__(self):
        return f"{self.name} Category"

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class SubCategory(IdentityTimeBaseModel):
    restaurant = models.ForeignKey(
        "merchant.Restaurant",
        on_delete=models.CASCADE,
        related_name="sub_categories",
        blank=True, null=True
    )
    name = models.CharField(
        max_length=500, unique=True
    )
    slug = AutoSlugField(populate_from="name", unique=True, null=True)
    description = models.CharField(
        max_length=500, blank=True, null=True
    )
    is_visible = models.BooleanField(default=True)
    category = models.ForeignKey(
        "Category",
        related_name="sub_categories",
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    image = models.ImageField(
        upload_to=MediaFolders.product_category_image_upload_to,
        blank=True, verbose_name="Product Category Image",
        null=True,
    )
    image_thumbnail = ImageSpecField(
        source="image",
        processors=[ResizeToFill(100, 100)],
        format="JPEG",
        options={"quality": 80}
    )
    image_thumbnail.short_description = "Thumbnail"

    def __str__(self):
        return f"{self.name} SubCategory"

    class Meta:
        verbose_name = "SubCategory"
        verbose_name_plural = "SubCategories"
