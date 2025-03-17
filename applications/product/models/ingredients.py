from django.db import models

from conf.core.models import IdentityTimeBaseModel


class Ingredient(IdentityTimeBaseModel):
    restaurant = models.ForeignKey(
        "merchant.Restaurant",
        on_delete=models.CASCADE,
        related_name="ingredients",
        blank=True, null=True
    )
    name = models.CharField(max_length=500)
    short_name = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.name
