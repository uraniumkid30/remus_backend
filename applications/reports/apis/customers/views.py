from rest_framework import viewsets
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from applications.reports.processors.orders import (
    total_orders_sold,
    total_orders
)


class ReportViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving reports.
    """
    permission_classes = [permissions.AllowAny]

    @extend_schema(operation_id="list reports", tags=["Reports"])
    def list(self, request):
        all_records: dict = {
            "records": [
                total_orders_sold,
                total_orders
            ]
        }
        return Response(all_records)
