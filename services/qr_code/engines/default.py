import io
from typing import Optional

import qrcode
from pydantic import BaseModel
from PIL.PngImagePlugin import PngImageFile

from services.qr_code.engines.logo import LogoEngine
from services.qr_code.engines.interface import (
    AbstractQRCodeConfigurationSchema,
    AbstractQRCodeEngine,
)


class QRImageConfigSchema(BaseModel):
    fill_color: Optional[str] = "Black"
    back_color: Optional[str] = "white"


class QRCodeConfigurationSchema(AbstractQRCodeConfigurationSchema):
    logo_name: str
    box_size: Optional[int] = 12
    border: Optional[int] = 1
    qr_image_config: Optional[QRImageConfigSchema] = QRImageConfigSchema()


class QRCodeEngine(AbstractQRCodeEngine):
    def get_qr_code_configuration(self, configuration: dict):
        return QRCodeConfigurationSchema(**configuration)

    def get_engine(self) -> qrcode.QRCode:
        """instantiates the engine used in creating the QRCode"""
        data = {
            "box_size": self.qr_code_config.box_size,
            "border": self.qr_code_config.border,
            "error_correction": qrcode.constants.ERROR_CORRECT_H,
        }
        return qrcode.QRCode(**data)

    def get_logo_data(self, logo_name, qr_image_size) -> dict:
        if not logo_name:
            return
        logo_raw_file: io.BytesIO = LogoEngine.get_custom_logo(logo_name)
        logo_file: PngImageFile = LogoEngine.create_logo(qr_image_size, logo_raw_file)
        logo_size: tuple = logo_file.size
        logo_position: tuple = LogoEngine.calculate_logo_position(
            logo_size, qr_image_size
        )
        return {
            "logo_file": logo_file,
            "logo_position": logo_position,
        }

    def create_qr_code(
        self,
        data: str,
    ) -> io.BytesIO:
        """Creates Qr code"""
        logo_name: str = self.qr_code_config.logo_name
        qr_image_name: str = self.qr_code_config.image_name
        qr_code_engine: qrcode.QRCode = self.get_engine()
        qr_code_engine.add_data(data)
        # generating QR code
        qr_code_engine.make()

        qr_image_config: QRImageConfigSchema = self.qr_code_config.qr_image_config
        # adding color to QR code
        qr_raw_image = qr_code_engine.make_image(**qr_image_config.dict()).convert(
            "RGB"
        )
        qr_image_size: tuple = qr_raw_image.size

        # handles logo
        logo_data: dict = self.get_logo_data(logo_name, qr_image_size)
        if logo_data:
            logo_file = logo_data["logo_file"]
            logo_position = logo_data["logo_position"]
            # adds logo to the qrcode
            qr_raw_image.paste(logo_file, logo_position)

        # returns the raw image file in bytes
        qr_image = io.BytesIO()
        qr_raw_image.save(qr_image, format="PNG")
        return qr_image.getvalue()
