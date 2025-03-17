from dataclasses import dataclass
from typing import Callable


def product_image_upload_to(self, filename):
    return f"products/{self.sub_category.name}/{filename}"


def product_category_upload(self, filename):
    return f"products/categories/{filename}"


@dataclass(frozen=True)
class MediaFolders:
    product_image_upload_to: Callable = product_image_upload_to
    product_category_image_upload_to: Callable = product_category_upload
