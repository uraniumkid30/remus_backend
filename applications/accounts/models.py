from datetime import datetime, timedelta

from django.db.models.functions import Now

import jwt
from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
)

from .media import MediaFolders
from .enums import UserRoles
from .managers.managers import UserManager, PinValidationManager
from conf.core.models import IdentityTimeBaseModel
from services.identifier import get_id_generator
from services.image_conversion.factory import get_image_service
from services.cloud.aws.s3 import S3Resource


class User(AbstractBaseUser, PermissionsMixin, IdentityTimeBaseModel):
    username = models.CharField(max_length=40, null=True, blank=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    phone_no = models.CharField(max_length=15, unique=True)
    role = models.CharField(
        max_length=50, choices=UserRoles.choices(), default=UserRoles.default()
    )
    email = models.EmailField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "phone_no"
    REQUIRED_FIELDS = [
        "email",
        "username",
    ]
    objects = UserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(minutes=120)

        token = jwt.encode(
            {"id": str(self.id), "exp": int(dt.strftime("%s"))},
            settings.SECRET_KEY,
            algorithm="HS256",
        )

        return token

    def get_full_name(self) -> str:
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self) -> str:
        """
        Returns the short name for the user.
        """
        return self.first_name

    def __str__(self):
        return "{}:{}".format(self.username, self.phone_no)


class Blacklist(IdentityTimeBaseModel):
    blacklist = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.blacklist


class UserProfile(IdentityTimeBaseModel):
    user = models.OneToOneField(to="User", on_delete=models.CASCADE)
    profile_picture = models.FileField(
        upload_to=MediaFolders.profile_picture, null=True, blank=True
    )
    restaurant = models.ForeignKey(
        "merchant.Restaurant",
        on_delete=models.CASCADE,
        related_name="workers",
        null=True,
        blank=True,
    )

    def __str__(self):
        return "Profile for : {}".format(self.user)

    def save(self, *args, **kwargs):
        self.convert_to_png()
        super().save(*args, **kwargs)

    def convert_to_png(self):
        if self.profile_picture and not self.profile_picture.name.endswith(".png"):
            processor = get_image_service("png")
            self.profile_picture = processor.convert_model_image(
                self.profile_picture,
                model_field_name="FileField",
            )

    def delete(self, *args, **kwargs):
        s3_agent = S3Resource()
        s3_agent.delete_object(self.profile_picture.name)
        super().delete(*args, **kwargs)


class Customer(IdentityTimeBaseModel):
    customer_id = models.CharField(max_length=40, null=True, blank=True)
    username = models.CharField(max_length=40, null=True, blank=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    phone_no = models.CharField(
        max_length=15, blank=True, null=True, unique=True, default=None
    )
    email = models.EmailField(unique=True, blank=True, null=True, default=None)

    def get_full_name(self) -> str:
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self) -> str:
        """
        Returns the short name for the user.
        """
        return self.first_name

    def __str__(self):
        return "{}:{}".format(self.username, self.phone_no)

    def save(self, *args, **kwargs):
        if not self.customer_id:
            id_generator = get_id_generator("randomstring")
            self.customer_id = id_generator.generate_id("USER", 4)
        super().save(*args, **kwargs)


class DeviceInfo(IdentityTimeBaseModel):
    user_agent = models.CharField(max_length=300, null=True, blank=True)
    browser_id = models.CharField(
        max_length=50,
        validators=[
            MinLengthValidator(10),
            MaxLengthValidator(10),
        ],
    )
    


class PinVerification(IdentityTimeBaseModel):
    registration_data = models.JSONField(default=dict)
    email = models.EmailField(unique=True)
    pin = models.CharField(
        max_length=6,
        validators=[
            MinLengthValidator(6),
            MaxLengthValidator(6),
        ],
        null=True,
        blank=True,
    )
    expires_at = models.DateTimeField(blank=True, null=True)
    objects = PinValidationManager()

    def save(self, *args, **kwargs):
        id_generator = get_id_generator("randomstring")
        self.pin = id_generator.generate_id(
            "",
            6,
            type="",
            use_seperator=False,
        )
        if not self.expires_at:
            self.expires_at = self.created_at or Now() + timedelta(days=1)
        super().save(*args, **kwargs)
