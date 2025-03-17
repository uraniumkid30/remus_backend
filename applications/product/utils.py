import uuid

from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from applications.order.models import TableSession
from .enums import ProductStatus


def is_available(product):
    verdict = product.status == ProductStatus.AVAILABLE
    if hasattr(product, "product_stocks"):
        return verdict and product.product_stocks.quantity > 0
    return verdict


def get_product_quantity_available(product):
    if hasattr(product, "product_stocks"):
        return product.product_stocks.quantity
    return None


def custom_query_params_check(query_params: dict):
    data = {}
    for item in query_params:
        if "session" == item:
            session_id = uuid.UUID(query_params[item])
            session = get_object_or_404(TableSession, id=session_id)
            if session.is_expired():
                raise ValidationError("Session is expired")
            data["restaurant"] = session.table.restaurant
        else:
            data[item] = query_params[item]
    return data
