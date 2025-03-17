import uuid

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema

from applications.order.models import Order
from .serializers import OrderSerializer
from conf.core.api.permissions import ReadOnlyProduct


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

    @extend_schema(operation_id="list orders for admin", tags=["Orders"])
    def list(self, request):
        queryset = self.get_queryset()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(operation_id="get order for admin", tags=["Orders"])
    def retrieve(self, request, pk=None):
        order = self.get_object()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    @extend_schema(operation_id="partially update order for admin", tags=["Orders"])
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
