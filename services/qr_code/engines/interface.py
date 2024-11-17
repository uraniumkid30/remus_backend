from abc import ABC, abstractmethod

from pydantic import BaseModel


class AbstractQRCodeConfigurationSchema(BaseModel):
    image_name: str


class AbstractQRCodeEngine(ABC):
    """Interface for all solid implementations"""

    def __init__(self, configuration: dict):
        qr_code_configuration: AbstractQRCodeConfigurationSchema = (
            self.get_qr_code_configuration(configuration)
        )
        self.qr_code_config = qr_code_configuration

    @abstractmethod
    def get_qr_code_configuration(
        self, configuration: dict
    ) -> AbstractQRCodeConfigurationSchema:
        """Creates a QRCode"""
        pass

    @abstractmethod
    def create_qr_code():
        """Creates a QRCode"""
        pass
