from rest_framework import viewsets
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import ValidationError

from applications.order.models import Order
from applications.order.apis.customers.serializers import (
    ReadOrderSerializer,
    OrderCheckoutSerializer,
)
from applications.order.utils import custom_query_params_check
from applications.order.apis.customers.documentation.schema import (
    ALL_ORDERS_SCHEMA,
    SINGLE_ORDER_SCHEMA,
    CREATE_ORDER_SCHEMA,
    ORDER_PAYMENT_REDIRECT,
)
from applications.payment.apis.customers.serializers import (
    PaymentSerializer,
)
from applications.payment.apis.customers.documentation.schema import (
    CREATE_PAYMENT_URL_SCHEMA,
)
from applications.payment.utils import PaymentHandler


class OrderViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving orders.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = ReadOrderSerializer

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
            self.api_session = query_params["session"]
            data = custom_query_params_check(query_params)
            data.pop("trxref", "")
            self.payment_reference = data.pop("reference", "")
            self.query_data = data
        return Order.objects.filter(**data)

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
        serializer = ReadOrderSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(**CREATE_ORDER_SCHEMA.to_dict())
    @action(detail=False, methods=["post"])
    def create_order(self, request, pk=None):
        self.get_queryset()
        request.data["table"] = self.query_data["table"]
        serializer = OrderCheckoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            try:
                table_name = serializer.validated_data["table"].name
                msg = f"New order from {table_name}."
            except Exception as err:
                msg = "New order from."
                print(err)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(**SINGLE_ORDER_SCHEMA.to_dict())
    def retrieve(self, request, pk=None):
        order = self.get_object()
        serializer = ReadOrderSerializer(order)
        return Response(serializer.data)

    # @extend_schema(operation_id="partially update order", tags=["Customer Orders"])
    # def partial_update(self, request, pk=None):
    #     self.get_queryset()
    #     request.data["table"] = self.query_data["table"]
    #     serializer = ReadOrderSerializer(data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     else:
    #         return Response(
    #             serializer.errors,
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

    @extend_schema(**CREATE_PAYMENT_URL_SCHEMA.to_dict())
    @action(detail=True, methods=["get"])
    def order_checkout(self, request, pk=None):
        self.get_queryset()
        try:
            p_handler = PaymentHandler(pk, self.api_session)
            url = p_handler.create_checkout_url()
            return redirect(url)
        except Exception as err:
            return Response(
                {"error": str(err)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @extend_schema(**ORDER_PAYMENT_REDIRECT.to_dict())
    @action(detail=True, methods=["get"])
    def payment_redirect(self, request, pk=None):
        self.get_queryset()
        try:
            p_handler = PaymentHandler(pk, self.api_session)
            res = p_handler.create_payment(self.payment_reference)
            #redirect to frontend url
            return Response(PaymentSerializer(res).data)
        except Exception as err:
            return Response(
                {"error": str(err)},
                status=status.HTTP_400_BAD_REQUEST,
            )
