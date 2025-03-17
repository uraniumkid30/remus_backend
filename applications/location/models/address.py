from django.db import models
from django.utils.translation import gettext_lazy as _

from conf.core.models import IdentityTimeBaseModel
from ..enums import States, Countries, CountryCode


class Address(IdentityTimeBaseModel):
    restaurant = models.OneToOneField(
        to="merchant.Restaurant", on_delete=models.CASCADE, related_name="address"
    )
    name = models.CharField(_("Address Name"), max_length=80, blank=True, null=True)
    address_1 = models.CharField(_("Address"), max_length=40, blank=False)
    address_2 = models.CharField(
        _("Address 2 (Optional)"), max_length=40, blank=True, null=True
    )
    locality = models.CharField(_("City"), max_length=40, blank=True, null=True)
    state = models.CharField(
        _("State"), max_length=40, choices=States.choices(), default=States.default()
    )
    country = models.CharField(
        _("Country/Region"),
        max_length=40,
        choices=Countries.choices(),
        default=Countries.default(),
    )
    country_code = models.CharField(
        _("CountryCode/RegionCode"),
        max_length=40,
        choices=CountryCode.choices(),
        default=CountryCode.default(),
    )
    zip_code = models.CharField(_("zip Code"), max_length=16, blank=True, null=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"{self.address_1} - {self.state} - {self.country}"

    class Meta:
        verbose_name = "address"
        verbose_name_plural = "addresses"

    def save(self, *args, **kwargs):
        self.name = f"{self.address_1}, {self.locality} {self.state}, {self.country}"
        super().save(*args, **kwargs)
