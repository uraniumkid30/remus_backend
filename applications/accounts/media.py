from typing import Callable
from dataclasses import dataclass


def profile_picture_upload_destination(instance, filename):
    return f"user_profiles/profile_picture/{instance.email}/{filename}"


def document_upload_destination(instance, filename):
    return f"user_profiles/documents/{instance.email}/{filename}"


@dataclass(frozen=True)
class MediaFolders:
    profile_picture: Callable = profile_picture_upload_destination
    documents: Callable = document_upload_destination
