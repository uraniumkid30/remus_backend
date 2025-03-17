from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import ValidationError

from applications.payment.models import Payment
from .serializers import PaymentSerializer
from applications.order.utils import custom_query_params_check
from .documentation.schema import (
    ALL_PAYMENTS_SCHEMA,
    SINGLE_PAYMENT_SCHEMA,
)


class PaymentViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving payments.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = PaymentSerializer

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
            data.pop("table", None)
            self.query_data = data
        return Payment.objects.filter(**data)

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        pk = self.kwargs.get("pk")
        if pk:
            filter["pk"] = pk
        obj = get_object_or_404(queryset, **filter)
        return obj

    @extend_schema(**ALL_PAYMENTS_SCHEMA.to_dict())
    def list(self, request):
        queryset = self.get_queryset()
        serializer = PaymentSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(**SINGLE_PAYMENT_SCHEMA.to_dict())
    def retrieve(self, request, pk=None):
        payment = self.get_object()
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)
