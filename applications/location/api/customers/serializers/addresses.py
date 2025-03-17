from rest_framework import serializers

from conf.core.serializers import EXCLUDED_TIME_FIELDS


from applications.location.models import (
    Address
)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = [*EXCLUDED_TIME_FIELDS]
