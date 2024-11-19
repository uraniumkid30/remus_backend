from dataclasses import dataclass


@dataclass(frozen=True)
class MediaFolders:
    logo: str = "merchant_assets/logos/"
    logo_inside_qr_code: str = "merchant_assets/qr_logos/"
    background: str = "merchant_assets/backgrounds/"
    qr_codes: str = "qrcodes/"
    site_favicon: str = "merchant_assets/favicons/"
