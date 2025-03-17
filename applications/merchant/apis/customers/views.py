from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import ValidationError

from applications.merchant.models import Restaurant
from applications.accounts.models import DeviceInfo
from applications.accounts.api.serializers import DeviceInfoSerializer
from .serializers import RestaurantSerializer
from applications.product.utils import custom_query_params_check


class RestaurantViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving restaurants.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = RestaurantSerializer
    lookup_url_kwarg = "slug"

    def get_queryset(self, **data):
        return Restaurant.objects.filter(**data)

    @extend_schema(operation_id="list restaurants", tags=["Restaurants"])
    def list(self, request):
        queryset = self.get_queryset()
        serializer = RestaurantSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(operation_id="get restaurant", tags=["Restaurants"])
    def retrieve(self, request, slug=None):
        queryset = self.get_queryset()
        restaurant = get_object_or_404(queryset, slug=slug)
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data)


class DeviceInfoViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving restaurants.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = DeviceInfoSerializer

    def get_queryset(self):
        return DeviceInfo.objects.all()

    @extend_schema(operation_id="get device_info", tags=["DeviceInfo"])
    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        restaurant = get_object_or_404(queryset, pk=pk)
        serializer = DeviceInfoSerializer(restaurant)
        return Response(serializer.data)
