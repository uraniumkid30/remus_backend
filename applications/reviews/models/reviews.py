from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from conf.core.models import IdentityTimeBaseModel


class ReviewRating(IdentityTimeBaseModel):
    table = models.ForeignKey(
        "merchant.Table",  on_delete=models.CASCADE,
        related_name="reviews",
        blank=True, null=True
    )
    order = models.ForeignKey(
        "order.Order",  on_delete=models.CASCADE,
        related_name="reviews",
        blank=True, null=True
    )
    subject = models.CharField(max_length=100, blank=True, null=True)
    review = models.TextField(blank=True, null=True)
    rating = models.PositiveSmallIntegerField(
        default=5,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    def __str__(self):
        return self.subject
