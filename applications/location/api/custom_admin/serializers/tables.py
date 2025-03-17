from rest_framework import serializers

from conf.core.serializers import EXCLUDED_TIME_FIELDS


from applications.merchant.models import (
    Table
)


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        exclude = [*EXCLUDED_TIME_FIELDS]
        read_only_fields = ["name", "restaurant"]
