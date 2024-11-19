
from django.core.files.base import ContentFile

from services.qr_code.engines import AbstractQRCodeEngine


class QRCodeGenerator:
    @staticmethod
    def generate_qr_code(data: str, qr_code_engine: AbstractQRCodeEngine):
        """calls a particular engine to creqate a QRCode"""
        qr_code = None
        try:
            qr_code = qr_code_engine.create_qr_code(data)
        except Exception as err:
            print(f"{err}")
        finally:
            return qr_code

    @staticmethod
    def save_qr_code(qr_code, file_name: str):
        """Handles saving of a QRCode"""
        return ContentFile(qr_code, file_name)
