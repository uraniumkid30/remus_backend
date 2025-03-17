from django.db import models
from django.db.models.functions import Now


class SessionManager(models.Manager):

    def get_queryset(self, *args, **kwargs):
        expired = super().get_queryset(*args, **kwargs).filter(
            expires_at__lt=Now()
        )
        expired.delete()
        return super().get_queryset(*args, **kwargs).filter(
            expires_at__gt=Now()
        )


class ExpiredSessionManager(models.Manager):

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            expires_at__lt=Now()
        )
