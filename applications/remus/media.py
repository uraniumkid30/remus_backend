from typing import Callable
from dataclasses import dataclass


def remus_logo(instance, filename):
    return f"remus/logos/{filename}"


def remus_logo_icon(instance, filename):
    return f"remus/logo_icons/{filename}"


@dataclass(frozen=True)
class MediaFolders:
    remus_logo: Callable = remus_logo
    remus_logo_icon: Callable = remus_logo_icon
