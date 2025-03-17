from rest_framework import serializers

from conf.core.serializers import EXCLUDED_TIME_FIELDS


from applications.product.models import (
    Ingredient
)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        exclude = ["id", *EXCLUDED_TIME_FIELDS]
