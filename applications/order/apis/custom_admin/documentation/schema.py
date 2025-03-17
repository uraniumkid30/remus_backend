from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
)

from .samples import (
    all_orders,
    single_order,
    order_id,
    update_payload,
    tag_name,
)
from ..serializers import OrderSerializer
from conf.core.api.schema_extensons import BaseSchema


ALL_ORDERS_SCHEMA = BaseSchema(
    operation_id="list orders for admin",
    description="get all orders from admin endpoint",
    tags=[tag_name],
    responses={
        200: OpenApiResponse(
            response=OrderSerializer,
            description="All Orders",
        ),
    },
    examples=[
        OpenApiExample(
            name="sample_request_data",
            value=all_orders,
            request_only=True,
        )
    ],
)

SINGLE_ORDER_SCHEMA = BaseSchema(
    operation_id="get order for admin",
    description="get a single order from admin endpoint",
    tags=[tag_name],
    parameters=[
        OpenApiParameter(
            name="id",
            description=order_id,
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.PATH,
        )
    ],
    responses={
        200: OpenApiResponse(
            response=OrderSerializer,
            description="Single Order",
        ),
    },
    examples=[
        OpenApiExample(
            name="sample_request_data",
            value=single_order,
            request_only=True,
        )
    ],
)

UPDATE_ORDER_SCHEMA = BaseSchema(
    operation_id="update an order for admin",
    description="Update an order from admin endpoint",
    tags=[tag_name],
    request=OrderSerializer,
    responses={
        200: OpenApiResponse(
            response=OrderSerializer,
            description="Updated Order",
        ),
    },
    examples=[
        OpenApiExample(
            name="sample_request_data",
            value=update_payload,
            request_only=True,
        )
    ],
)
