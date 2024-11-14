import re
import logging

from rest_framework import serializers
from django.contrib.auth import authenticate

from ..models import User, UserProfile
from .validators import FieldValidators
from ..managers.services import UserService


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
    is_verified = serializers.CharField(max_length=255, allow_blank=True, read_only=True)

    def validate_username(self, value):
        list_of_validators = [
            FieldValidators.is_phone_no_valid(value),
            FieldValidators.is_email_valid(value),
            FieldValidators.is_username_valid(value),
        ]
        if not value:
            raise serializers.ValidationError(
                'Username, Email, Phone is required to log in.'
            )
        elif not any(list_of_validators):
            raise serializers.ValidationError(
                'Username, Email, Phone is invalid.'
            )
        return value

    def validate_password(self, value):
        if value is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        return value


class DashboardSerializer(serializers.Serializer):
    pass


class RegistrationSerializer(serializers.Serializer):
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
            raise serializers.ValidationError(
                'An phone_no is required.'
            )
        elif not FieldValidators.is_phone_no_valid(value):
            raise serializers.ValidationError(
                'Phone_no is invalid.'
            )
        return value

    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError(
                'An password is required.'
            )
        elif not FieldValidators.is_password_valid(value):
            raise serializers.ValidationError(
                'Password is invalid.'
            )
        return value

    def create(self, validated_data):
        return UserService.create_user(data=validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'first_name',
            'last_name', 'email',
            'phone_no', ]
        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'phone_no': {
                'required': False,
                'allow_blank': True,
                'allow_null': True
            }
        }


class ProfileUpdateSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['user']

    def swap(self, value, new):
        if value:
            return value
        else:
            return new

    def clean_phone_no(self, phone_no):
        if not (phone_no.startswith('0') or re.match('\+?234', phone_no)):
            phone_no = '0' + phone_no
        return phone_no

    def update(self, instance, validated_data):
        validated_data = validated_data['user']
        instance.user.email = self.swap(validated_data.get('email'), instance.user.email)
        instance.user.first_name = self.swap(validated_data.get('first_name'), instance.user.first_name)
        instance.user.last_name = self.swap(validated_data.get('last_name'), instance.user.last_name)
        phone_no = self.swap(validated_data.get('phone_no'), instance.user.phone_no)
        instance.user.phone_no = self.clean_phone_no(phone_no)
        instance.user.save()
        return instance


class PasswordResetSerializer(serializers.Serializer):
    phone_no = serializers.CharField(max_length=255, write_only=True)


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    confirm_password = serializers.CharField(max_length=128, write_only=True)
    email = serializers.CharField(max_length=255, write_only=True)


class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'first_name',
            'last_name', 'phone_no',
            'email', 'is_active',
            'created_at',
        )
