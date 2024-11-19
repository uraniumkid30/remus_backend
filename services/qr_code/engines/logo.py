import io
from typing import Tuple

from PIL import Image
from PIL.PngImagePlugin import PngImageFile

from services.qr_code.engines.storage import CustomStorage


class LogoEngine:
    @staticmethod
    def get_custom_logo(
        logo_name: str,
    ) -> io.BytesIO:
        """calls storage class to hanfle everything about logo name finding"""
        storage = CustomStorage.get_storage(logo_name)
        logofile = storage.open(name=logo_name)
        CustomStorage.reset_storage_location()
        logofile_raw = logofile.read()
        logo_raw_file = io.BytesIO(logofile_raw)
        return logo_raw_file

    @staticmethod
    def create_logo(qr_image_size: tuple, logo_raw_file: io.BytesIO) -> PngImageFile:
        """creates the logo and resizes it, after it has been found"""

        logo: PngImageFile = Image.open(logo_raw_file)
        logo_size = logo.size
        logo: PngImageFile = LogoEngine.resize_logo(logo, logo_size, qr_image_size)
        return logo

    @staticmethod
    def resize_logo(
        logo: PngImageFile, logo_size: tuple, qr_image_size: tuple
    ) -> PngImageFile:
        """compares the size of the logo with the size of the qrcode, resizes the logo if needed"""
        lower_ratio_limit: float = 0.08
        upper_ratio_limit: float = 0.14
        logo_width, logo_height = logo_size
        qr_image_width, qr_image_height = logo_size
        width_ratio: float = logo_width / qr_image_width
        height_ratio: float = logo_height / qr_image_height
        if width_ratio > lower_ratio_limit:
            logo_width *= lower_ratio_limit if width_ratio > 0.5 else upper_ratio_limit
            logo_width = int(logo_width)
        if height_ratio > lower_ratio_limit:
            logo_height *= (
                lower_ratio_limit if height_ratio > 0.5 else upper_ratio_limit
            )
            logo_height = int(logo_height)
        return logo.resize((logo_width, logo_height), Image.LANCZOS)

    @staticmethod
    def calculate_logo_position(
        logo_size: tuple, qr_image_size: tuple
    ) -> Tuple[int, int]:
        """determines where to position the logo"""
        logo_width, logo_height = logo_size
        qr_image_width, qr_image_height = qr_image_size
        width: int = (qr_image_width - logo_width) // 2
        height: int = (qr_image_height - logo_height) // 2
        return (width, height)
