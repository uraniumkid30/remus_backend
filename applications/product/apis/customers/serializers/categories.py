from rest_framework import serializers

from conf.core.serializers import EXCLUDED_TIME_FIELDS

from .ingredients import IngredientSerializer
from .products import RelatedProductSerializer
from applications.product.models import SubCategory, Category, Product
from applications.product.utils import get_product_quantity_available, is_available


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = [*EXCLUDED_TIME_FIELDS]


class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = SubCategory
        exclude = [*EXCLUDED_TIME_FIELDS]


class ProductSerializer(serializers.ModelSerializer):
    sub_category = SubCategorySerializer()
    ingredients = IngredientSerializer(many=True)
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


class RelatedSubCategorySerializer(serializers.ModelSerializer):
    products = RelatedProductSerializer(many=True, read_only=True)

    class Meta:
        model = SubCategory
        fields = ["id", "name", "slug", "description", "image", "products"]


class RelatedCategorySerializer(serializers.ModelSerializer):
    sub_categories = RelatedSubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "image", "sub_categories"]
