from rest_framework import serializers

from conf.core.serializers import EXCLUDED_TIME_FIELDS

from applications.location.api.customers.serializers import AddressSerializer
from applications.merchant.models import (
    Restaurant,
    OperationSchedule,
    SocialAccount,
    RestaurantPlatformSettings,
)


class OperationScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationSchedule
        exclude = [*EXCLUDED_TIME_FIELDS]


class SocialAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAccount
        exclude = [*EXCLUDED_TIME_FIELDS]


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantPlatformSettings
        exclude = [*EXCLUDED_TIME_FIELDS]


class RestaurantSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    operation_schedules = OperationScheduleSerializer(many=True, read_only=True)
    social_accounts = SocialAccountSerializer(many=True, read_only=True)
    platform_setting = PlatformSerializer(read_only=True)

    class Meta:
        model = Restaurant
        exclude = [*EXCLUDED_TIME_FIELDS]
