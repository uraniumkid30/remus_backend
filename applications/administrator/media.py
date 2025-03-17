from typing import Callable
from dataclasses import dataclass


def administrator_logo(instance, filename):
    return f"administrator/logos/{filename}"


def administrator_logo_icon(instance, filename):
    return f"administrator/logo_icons/{filename}"


def administrator_thumbnail(instance, filename):
    return f"administrator/test_thumbnail/{filename}"


def administrator_cir_thumbnail(instance, filename):
    return f"administrator/test_circular_thumbnail/{filename}"


@dataclass(frozen=True)
class MediaFolders:
    administrator_logo: Callable = administrator_logo
    administrator_logo_icon: Callable = administrator_logo_icon
    administrator_cir_thumbnail: Callable = administrator_cir_thumbnail
    administrator_thumbnail: Callable = administrator_thumbnail
