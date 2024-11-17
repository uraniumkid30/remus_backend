from datetime import datetime, timedelta

import jwt
from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from .media import MediaFolders
from .enums import (
    UserRoles, VerificationStatus,
    DocumentTypes,
    DocumentCategories
)
from .managers.managers import UserManager
from conf.core.models import IdentityTimeBaseModel


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
    REQUIRED_FIELDS = ["email", "username", ]
    objects = UserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=365)

        token = jwt.encode({
            "id": str(self.id),
            "exp": int(dt.strftime("%s"))
        }, settings.SECRET_KEY, algorithm="HS256")

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
    verification_status = models.CharField(
        max_length=50, choices=VerificationStatus.choices(),
        default=VerificationStatus.default()
    )
    verification_comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return "Profile for : {}".format(self.user)


class Documents(IdentityTimeBaseModel):
    user = models.ForeignKey(
        to="User",
        on_delete=models.CASCADE,
        related_name="documents",
    )
    document_type = models.CharField(
        max_length=100,
        choices=DocumentTypes.choices(),
        default=DocumentTypes.default()
    )
    document_category = models.CharField(
        max_length=100,
        choices=DocumentCategories.choices(),
        default=DocumentCategories.default()
    )
    docunment_number = models.CharField(max_length=255, blank=True, null=True)
    upload = models.FileField(
        upload_to=MediaFolders.documents, null=True, blank=True
    )

    def __str__(self):
        return "Documents for : {}".format(self.user)
