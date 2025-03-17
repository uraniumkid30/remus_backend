from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import ValidationError

from applications.product.models import Product, Category
from .serializers import ProductSerializer, RelatedCategorySerializer
from applications.product.utils import custom_query_params_check
from applications.product.apis.customers.documentation.schema import (
    ALL_PRODUCTS_SCHEMA,
    SINGLE_PRODUCT_SCHEMA,
    ALL_CATEGORY_SCHEMA,
    SINGLE_CATEGORY_SCHEMA,
    ALL_RCATEGORY_SCHEMA,
    SINGLE_RCATEGORY_SCHEMA,
)


class ProductViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving products.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = ProductSerializer

    def get_queryset(self):
        query_params = self.request.query_params
        if len(query_params) < 1:
            raise ValidationError(
                {"Error": "query missing required amount of query fields"}
            )
        elif "session" not in query_params:
            raise ValidationError(
                {"Error": "query_params missing session field and value"}
            )
        else:
            data = custom_query_params_check(query_params)
        return Product.objects.filter(**data)

    @extend_schema(**ALL_PRODUCTS_SCHEMA.to_dict())
    def list(self, request):
        queryset = self.get_queryset()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(**SINGLE_PRODUCT_SCHEMA.to_dict())
    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        product = get_object_or_404(queryset, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving products.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = RelatedCategorySerializer
    lookup_url_kwarg = "id"

    def get_queryset(self):
        query_params = self.request.query_params
        if len(query_params) < 1:
            raise ValidationError(
                {"Error": "query missing required amount of query fields"}
            )
        elif "session" not in query_params:
            raise ValidationError(
                {"Error": "query_params missing session field and value"}
            )
        else:
            data = custom_query_params_check(query_params)
        return Category.objects.filter(**data)

    @extend_schema(**ALL_CATEGORY_SCHEMA.to_dict())
    def list(self, request):
        queryset = self.get_queryset()
        serializer = RelatedCategorySerializer(queryset, many=True)
        res = Response(serializer.data)
        return res

    @extend_schema(**SINGLE_CATEGORY_SCHEMA.to_dict())
    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        category = get_object_or_404(queryset, pk=pk)
        serializer = RelatedCategorySerializer(category)
        return Response(serializer.data)


class RestaurantCategoryViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving categories.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = RelatedCategorySerializer
    lookup_url_kwarg = "id"

    def get_queryset(self, restaurant_id):
        return Category.objects.filter(restaurant=restaurant_id)

    @extend_schema(**ALL_RCATEGORY_SCHEMA.to_dict())
    def list(self, request, restaurant_id=None):
        queryset = self.get_queryset(restaurant_id)
        serializer = RelatedCategorySerializer(queryset, many=True)
        res = Response(serializer.data)
        return res

    @extend_schema(**SINGLE_RCATEGORY_SCHEMA.to_dict())
    def retrieve(self, request, restaurant_id=None, pk=None):
        queryset = self.get_queryset(restaurant_id)
        category = get_object_or_404(queryset, pk=pk)
        serializer = RelatedCategorySerializer(category)
        return Response(serializer.data)
