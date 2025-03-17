from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema

from applications.order.models import Order
from .serializers import OrderSerializer
from conf.core.api.permissions import ReadOnlyProduct
from .documentation.schema import (
    ALL_ORDERS_SCHEMA,
    SINGLE_ORDER_SCHEMA,
    UPDATE_ORDER_SCHEMA
)


class OrderViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving orders.
    """
    permission_classes = [ReadOnlyProduct]
    serializer_class = OrderSerializer

    def get_queryset(self):
        query_params = self.request.query_params
        data = {}
        for item in query_params:
            data[item] = query_params[item]
        return Order.objects.filter(**data).order_by("-created_at")

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        pk = self.kwargs.get("pk")
        if pk:
            filter["pk"] = pk
        obj = get_object_or_404(queryset, **filter)
        return obj

    @extend_schema(**ALL_ORDERS_SCHEMA.to_dict())
    def list(self, request):
        queryset = self.get_queryset()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(**SINGLE_ORDER_SCHEMA.to_dict())
    def retrieve(self, request, pk=None):
        order = self.get_object()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    @extend_schema(**UPDATE_ORDER_SCHEMA.to_dict())
    def partial_update(self, request, pk=None):
        serializer = OrderSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    # @extend_schema(operation_id="delete order", tags=["Orders"])
    # def destroy(self, request, pk=None):
    #     order = self.get_object()
    #     order.delete()
    #     return Response(
    #         {"message": "Order Deleted!"},
    #         status=status.HTTP_204_NO_CONTENT
    #     )
