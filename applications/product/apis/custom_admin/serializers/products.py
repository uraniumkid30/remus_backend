from rest_framework import serializers

from applications.product.models import Product
from conf.core.serializers import EXCLUDED_TIME_FIELDS
from .ingredients import IngredientSerializer
from .discounts import DiscountSerializer
from applications.product.utils import get_product_quantity_available, is_available


class RelatedProductSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    discount = DiscountSerializer(many=True)
    is_available = serializers.SerializerMethodField()
    quantity_available = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "sub_category",
            "chef",
            "ingredients",
            "discount",
            "name",
            "slug",
            "description",
            "point",
            "unit_price",
            "wait_time",
            "image",
            # "image_thumbnail",
            "is_available",
            "quantity_available",
        ]

    def get_is_available(self, obj):
        return is_available(obj)

    def get_quantity_available(self, obj):
        return get_product_quantity_available(obj)
