import uuid
from datetime import datetime
from typing import NoReturn, List

from django.db import models


class TimeBaseModel(models.Model):
    """
    This model defines base models that implements common fields like:
    created_at
    updated_at
    is_deleted
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def soft_delete(self: object) -> NoReturn:
        """Soft delete a model instance"""
        self.is_deleted: bool = True
        self.deleted_at: datetime = datetime.now()
        self.save()

    class Meta:
        abstract: bool = True
        ordering: List[str] = ['-created_at']


class IdentityTimeBaseModel(TimeBaseModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )

    class Meta(TimeBaseModel.Meta):
        abstract: bool = True
