from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema

from applications.product.models import Product, Category
from .serializers import AdminProductSerializer, RelatedCategorySerializer
from conf.core.api.permissions import ReadOnlyProduct
from applications.product.apis.custom_admin.documentation.schema import (
    ALL_PRODUCTS_SCHEMA,
    SINGLE_PRODUCT_SCHEMA,
    ALL_CATEGORY_SCHEMA,
    SINGLE_CATEGORY_SCHEMA,
)


class ProductViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving products.
    """

    permission_classes = [ReadOnlyProduct]
    serializer_class = AdminProductSerializer

    def get_queryset(self):
        return Product.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        pk = self.kwargs.get("pk")
        if pk:
            filter["pk"] = pk
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

    @extend_schema(**ALL_PRODUCTS_SCHEMA.to_dict())
    def list(self, request):
        queryset = self.get_queryset()
        serializer = AdminProductSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(**SINGLE_PRODUCT_SCHEMA.to_dict())
    def retrieve(self, request, pk=None):
        product = self.get_object()
        serializer = AdminProductSerializer(product)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving products.
    """

    permission_classes = [ReadOnlyProduct]
    serializer_class = RelatedCategorySerializer

    def get_queryset(self):
        return Category.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        pk = self.kwargs.get("pk")
        if pk:
            filter["pk"] = pk
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

    @extend_schema(**ALL_CATEGORY_SCHEMA.to_dict())
    def list(self, request):
        queryset = self.get_queryset()
        serializer = RelatedCategorySerializer(queryset, many=True)
        res = Response(serializer.data)
        return res

    @extend_schema(**SINGLE_CATEGORY_SCHEMA.to_dict())
    def retrieve(self, request, pk=None):
        category = self.get_object()
        serializer = RelatedCategorySerializer(category)
        return Response(serializer.data)
