from typing import NoReturn

from django.conf import settings
from django.core.files.storage import default_storage


class CustomStorage:
    __STORAGE = default_storage
    previous_storage_location = ""

    @staticmethod
    def is_dev_environment() -> bool:
        """boolean which indicates if settings env is a dev environment"""
        return False if getattr(settings, "STATIC_URL", "").find("http") >= 0 else True

    @staticmethod
    def is_background_logo(logo_name: str) -> bool:
        """boolean which indicates if logo is a background image or user custom image"""
        return True if settings.DEFAULT_REMUS_LOGO in logo_name else False

    @staticmethod
    def storage_location_factory(logo_name: str) -> str:
        """Handles which location to send to storage"""
        background_logo: bool = CustomStorage.is_background_logo(logo_name)
        dev_environment: bool = CustomStorage.is_dev_environment()
        if dev_environment and background_logo:
            location = "staticfiles"
        elif dev_environment and not background_logo:
            location = f"{settings.MEDIA_DIR}"
        elif not dev_environment and background_logo:
            location = "static"
        elif not dev_environment and not background_logo:
            location = "media"
        return location

    @classmethod
    def get_storage(cls, logo_name: str) -> str:
        """Gets storage location"""
        new_storage_location = CustomStorage.storage_location_factory(logo_name)
        cls.previous_storage_location = cls.__STORAGE.location
        cls.__STORAGE.location = new_storage_location
        return cls.__STORAGE

    @classmethod
    def reset_storage_location(cls) -> NoReturn:
        """You must reset your storage location"""
        cls.__STORAGE.location = cls.previous_storage_location
