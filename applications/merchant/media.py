from dataclasses import dataclass
from typing import Callable


base = "merchant_assets"


class RestaurantCallable:
    @staticmethod
    def logo(instance, filename):
        return f"{base}/logos/restaurant/{instance.name}/{filename}"

    @staticmethod
    def logo_inside_qr_code(instance, filename):
        return f"{base}/qr_logos/{instance.name}/{filename}"

    @staticmethod
    def background(instance, filename):
        return f"{base}/backgrounds/{instance.name}/{filename}"

    @staticmethod
    def site_favicon(instance, filename):
        return f"{base}/favicons/restaurant/{instance.name}/{filename}"

    @staticmethod
    def receipt_thumbnail(instance, filename):
        return f"{base}/receipt_thumbnail/{instance.name}/{filename}"

    @staticmethod
    def social_logo(instance, filename):
        return f"{base}/social_logo/{instance.name}/{filename}"

    @staticmethod
    def qrcodes(instance, filename):
        return f"{base}/qrcodes/{instance.table.name}/{filename}"


class MerchantCallable:
    @staticmethod
    def logo(instance, filename):
        return f"{base}/logos/merchant/{instance.name}/{filename}"

    @staticmethod
    def site_favicon(instance, filename):
        return f"{base}/favicons/merchant/{instance.name}/{filename}"


@dataclass(frozen=True)
class MerchantMediaFolders:
    logo: Callable = MerchantCallable.logo
    site_favicon: Callable = MerchantCallable.site_favicon


@dataclass(frozen=True)
class RestaurantMediaFolders:
    logo: Callable = RestaurantCallable.logo
    logo_inside_qr_code: Callable = RestaurantCallable.logo_inside_qr_code
    background: Callable = RestaurantCallable.background
    qr_codes: Callable = RestaurantCallable.qrcodes
    site_favicon: Callable = RestaurantCallable.site_favicon
    receipt_thumbnail: Callable = RestaurantCallable.receipt_thumbnail
    social_logo: Callable = RestaurantCallable.social_logo
