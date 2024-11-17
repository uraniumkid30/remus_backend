from typing import Union, NoReturn

from django.conf import settings
from django.core.files.storage import DefaultStorage
from django.db import models

from ..enums import PosProvider
from ..media import MediaFolders
from conf.core.models import IdentityTimeBaseModel
from services.crypto import generate_terminal_id


class Company(IdentityTimeBaseModel):
    name = models.CharField(max_length=200, )
    company_id = models.CharField(max_length=20, default="111111-1111")
    phone_office = models.CharField(
        "Telephone", max_length=20, blank=True, null=True
    )
    phone_mobile = models.CharField(
        "Mobile Phone", max_length=20, blank=True, null=True
    )
    email = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class MerchantProfile(IdentityTimeBaseModel):
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="merchants"
    )
    company = models.ForeignKey(
        "Company",
        on_delete=models.CASCADE,
        related_name="merchants",
        null=True, blank=True
    )
    website = models.URLField()
    name = models.CharField(max_length=256)
    display_name = models.CharField(max_length=32)
    tax_id = models.CharField(max_length=32, null=True, blank=True)
    vat_id = models.CharField(max_length=32, null=True, blank=True)
    logo = models.FileField(
        upload_to=MediaFolders.logo, null=True, blank=True
    )
    logo_inside_qr_code = models.FileField(
        upload_to=MediaFolders.logo_inside_qr_code, null=True, blank=True
    )
    background = models.FileField(
        upload_to=MediaFolders.background, null=True, blank=True
    )
    custom_link = models.CharField(max_length=350, null=True, blank=True)

    def __str__(self):
        return self.name


class Store(IdentityTimeBaseModel):
    merchant = models.ForeignKey(
        "MerchantProfile", on_delete=models.CASCADE, related_name="stores"
    )
    address = models.CharField(max_length=256, blank=True)
    opening_times = models.CharField(max_length=256, blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    merchant_store_id = models.CharField(
        max_length=128, null=True, blank=True,
        help_text="Store ID used by the merchant"
    )
    merchant_store_name = models.CharField(
        max_length=128, null=True, blank=True,
        help_text="Store name used by the merchant"
    )

    def __str__(self):
        return f"{self.merchant.name} {self.address}"


class PointOfSale(IdentityTimeBaseModel):
    store = models.ForeignKey(
        "Store", on_delete=models.CASCADE, related_name="points_of_sale"
    )
    version = models.CharField(max_length=32, null=True, blank=True)
    terminal_id = models.CharField(
        max_length=50, default=generate_terminal_id, unique=True
    )
    provider = models.CharField(
        max_length=64,
        choices=PosProvider.choices(),
        default=PosProvider.default()
    )

    def __str__(self):
        return f"POS Terminal ID: {self.terminal_id} in Store: {self.store}"


qr_storage = DefaultStorage()

if not settings.DEBUG:
    from conf.storage_backends import MediaAttachmentStorage

    qr_storage = MediaAttachmentStorage()


class QRTag(IdentityTimeBaseModel):
    point_of_sale = models.ForeignKey(
        "PointOfSale", on_delete=models.SET_NULL,
        related_name="qr_links", blank=True,
        null=True
    )
    position = models.CharField(max_length=64, blank=True, null=True)
    qr_image = models.FileField(
        upload_to=MediaFolders.qr_codes, editable=False, null=True,
        storage=qr_storage
    )
    domain = models.CharField(
        max_length=128, blank=True, null=True, editable=False
    )

    def is_available(self):
        return self.point_of_sale is None

    def get_pos_provider(self):
        return self.point_of_sale.provider

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("merchant:qr_request_receipt", args=[str(self.id)])

    def get_merchant_domain(self):
        from merchant.utils.urls import merchant_domain
        if self.domain:
            return self.domain
        try:
            store = self.point_of_sale.store
        except Exception:
            store = None
        return merchant_domain(store)

    def get_merchant_qr_logo(self) -> Union[str, None]:
        """Returns the name of the logo and the root location of the file"""
        try:
            result = ""
            merchant = self.point_of_sale.store.merchant
            logo = merchant.logo_inside_qr_code
            if logo:
                result = logo.name
        except Exception as err:
            print(f"error {err}")
        finally:
            return result

    def _create_qr_image(self) -> NoReturn:
        from services.qr_code import QRCodeGenerator
        from services.qr_code.engines import QRCodeEngine

        logo_id: str = self.get_merchant_qr_logo()
        base_url: str = self.get_merchant_domain()

        data: str = f"https://{base_url}{self.get_absolute_url()}"
        file_name: str = f"qr-{self.id}.png"
        configuration: dict = {
            "image_name": file_name,
            "logo_name": logo_id,
        }
        qr_code_engine: QRCodeEngine = QRCodeEngine(configuration)
        qr_code = QRCodeGenerator.generate_qr_code(
            data=data, qr_code_engine=qr_code_engine
        )
        if qr_code:
            saved_qr_code = QRCodeGenerator.save_qr_code(qr_code, file_name)
            self.qr_image = saved_qr_code

    def save(self, *args, **kwargs):
        if not self.qr_image:
            self._create_qr_image()
            self.domain = self.get_merchant_domain()
        super().save(*args, **kwargs)

    def __str__(self):
        created_at_str = self.created_at.strftime("%Y-%m-%d %H:%M")
        default: str = f" at Position: {self.position}"
        qr_position = '' if self.position is None else default
        id_str = str(self.id)
        display_id = f"{id_str[:4]}...{id_str[-4:]}"
        result = f"QRTag {display_id} created at {created_at_str}. "
        result += f"Placed at {self.point_of_sale}{qr_position}"
        return result
