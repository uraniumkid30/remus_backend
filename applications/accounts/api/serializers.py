import logging

from rest_framework import serializers
from django.template.loader import render_to_string

from ..models import User, DeviceInfo, Customer, PinVerification
from .validators import FieldValidators
from conf.core.serializers import EXCLUDED_TIME_FIELDS
from applications.accounts.managers.services import UserService
from applications.accounts.permissions import get_role_permissions
from services.email_dispatcher import email_engine_factory


logger = logging.getLogger(__name__)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=225,
        error_messages={
            "required": " username, email or phone_no is required ",
        },
        write_only=True,
    )
    password = serializers.CharField(max_length=128, write_only=True)
    verification_token = serializers.CharField(
        max_length=255, allow_blank=True, required=False
    )

    # Ignore these fields if they are included in the request.
    phone_no = serializers.CharField(max_length=255, read_only=True)
    token = serializers.CharField(max_length=400, read_only=True)
    is_verified = serializers.CharField(
        max_length=255, allow_blank=True, read_only=True
    )

    def validate_username(self, value):
        list_of_validators = [
            FieldValidators.is_phone_no_valid(value),
            FieldValidators.is_email_valid(value),
            FieldValidators.is_username_valid(value),
        ]
        if not value:
            raise serializers.ValidationError(
                "Username, Email, Phone is required to log in."
            )
        elif not any(list_of_validators):
            raise serializers.ValidationError("Username, Email, Phone is invalid.")
        return value

    def validate_password(self, value):
        if value is None:
            raise serializers.ValidationError("A password is required to log in.")
        return value


class InitiateRegistrationSerializer(serializers.Serializer):
    phone_no = serializers.CharField(
        error_messages={
            "required": "phone_number is required to aid notifications",
        },
        write_only=True,
    )
    username = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    first_name = serializers.CharField(max_length=255, write_only=True)
    last_name = serializers.CharField(max_length=255, write_only=True)
    email = serializers.EmailField(max_length=255, write_only=True)

    def validate_phone_no(self, value):
        if not value:
            raise serializers.ValidationError("An phone_no is required.")
        elif not FieldValidators.is_phone_no_valid(value):
            raise serializers.ValidationError("Phone_no is invalid.")
        return value

    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError("An password is required.")
        elif not FieldValidators.is_password_valid(value):
            raise serializers.ValidationError(
                "Password is invalid. Must contain Uppercase, lowercase, numbers and symbols"
            )
        return value

    def create(self, validated_data):
        email = validated_data.get("email")
        try:
            pin_ver = PinVerification.objects.get(email=email)
            pin_ver.email = email
            pin_ver.save()
        except PinVerification.DoesNotExist:
            pin_ver = PinVerification.objects.create(
                registration_data=validated_data,
                email=email,
            )
        finally:
            full_name = f'{validated_data.get("first_name")} '
            full_name += f'{validated_data.get("last_name")}'
            body2 = render_to_string(
                "registration.html",
                {
                    "first_name": validated_data.get("first_name"),
                    "last_name": validated_data.get("last_name"),
                    "pin": pin_ver.pin,
                },
            )
            data = {
                "body": body2,
                "subject": "Welcome to Remus",
                "sender_name": "remus",
                "to_name": full_name,
            }
            to = [{"name": full_name, "email": email}]
            _from = "remus@noreply.com"
            cl = email_engine_factory("sentinel")
            cl.send_mail(to, _from, **data)
            return pin_ver


class RegistrationSerializer(serializers.Serializer):
    pin = serializers.CharField(
        error_messages={
            "required": "pin is required to aid notifications",
        },
        write_only=True,
    )
    email = serializers.EmailField(max_length=255, write_only=True)

    def find_pin(self, data):
        pin = data.get("pin")
        email = data.get("email")
        try:
            return PinVerification.objects.get(email=email, pin=pin)

        except PinVerification.DoesNotExist:
            return None

    def create(self, validated_data):
        pin_data = self.find_pin(
            {
                "email": validated_data.get("email"),
                "pin": validated_data.get("pin"),
            }
        )
        user = UserService.create_user(data=pin_data.registration_data)
        pin_data.delete()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "phone_no", "role"]
        extra_kwargs = {
            "id": {"read_only": True},
            "phone_no": {"required": False, "allow_blank": True, "allow_null": True},
        }

    def to_representation(self, instance):
        data = super(UserSerializer, self).to_representation(instance)
        data["permissions"] = get_role_permissions(instance.role)
        return data


class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "phone_no",
            "email",
            "is_active",
            "role",
            "created_at",
        )


class DeviceInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceInfo
        exclude = [*EXCLUDED_TIME_FIELDS]
        extra_kwargs = {
            "id": {"read_only": True},
            "browser_id": {"required": True},
        }


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = [*EXCLUDED_TIME_FIELDS]
        extra_kwargs = {
            "customer_id": {"required": False, "allow_blank": True, "allow_null": True},
            "phone_no": {"required": False, "allow_blank": True, "allow_null": True},
            "email": {"required": True},
            "first_name": {"required": False},
            "last_name": {"required": False},
        }


def login_data(data, user):
    return {
        "status": "00",
        "token": user.token,
        "id": data["id"],
        "permissions": data["permissions"],
    }
