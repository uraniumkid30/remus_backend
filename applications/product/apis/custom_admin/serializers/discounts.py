from rest_framework import serializers

from conf.core.serializers import EXCLUDED_TIME_FIELDS


from applications.product.models import (
    Discount
)


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        exclude = ["id", *EXCLUDED_TIME_FIELDS]
