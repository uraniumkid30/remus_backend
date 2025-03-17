from dataclasses import dataclass
from typing import Callable


def receipt_files(instance, filename):
    return f"payments/receipts/{filename}"


@dataclass(frozen=True)
class MediaFolders:
    receipt_file: Callable = receipt_files
