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
    checkout_payload,
    tag_name,
)
from ..serializers import ReadOrderSerializer, OrderCheckoutSerializer
from conf.core.api.schema_extensons import (
    BaseSchema,
    session_q_params,
    reference_q_params,
)
from conf.core.serializers import ErrorSerializer


ALL_ORDERS_SCHEMA = BaseSchema(
    operation_id="list orders",
    description="get all orders",
    tags=[tag_name],
    parameters=[
        session_q_params,
    ],
    responses={
        200: OpenApiResponse(
            response=ReadOrderSerializer,
            description="All Orders",
        ),
    },
    examples=[
        OpenApiExample(
            name="sample_response_data",
            value=all_orders,
            response_only=True,
        )
    ],
)

SINGLE_ORDER_SCHEMA = BaseSchema(
    operation_id="get order",
    description="get a single order",
    tags=[tag_name],
    parameters=[
        OpenApiParameter(
            name="id",
            description=order_id,
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.PATH,
        ),
        session_q_params,
    ],
    responses={
        200: OpenApiResponse(
            response=ReadOrderSerializer,
            description="Single Order",
        ),
    },
    examples=[
        OpenApiExample(
            name="sample_response_data",
            value=single_order,
            response_only=True,
        )
    ],
)

CREATE_ORDER_SCHEMA = BaseSchema(
    operation_id="create an order",
    description="Checkout all cart or order items",
    tags=[tag_name],
    request=OrderCheckoutSerializer,
    parameters=[
        session_q_params,
    ],
    responses={
        200: OpenApiResponse(
            response=ReadOrderSerializer,
            description="Created Order",
        ),
    },
    examples=[
        OpenApiExample(
            name="sample_request_data",
            value=checkout_payload,
            request_only=True,
        ),
        OpenApiExample(
            name="sample_response_data",
            value=single_order,
            response_only=True,
        ),
    ],
)


ORDER_PAYMENT_REDIRECT = BaseSchema(
    operation_id="order payment callback url",
    description="callback url  payment service will call after paayment has been made by customer",
    tags=[tag_name],
    parameters=[
        OpenApiParameter(
            name="id",
            description=order_id,
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.PATH,
        ),
        session_q_params,
        reference_q_params,
    ],
    responses={
        302: OpenApiResponse(
            # response=ReadOrderSerializer,
            description="Payment service call back url, redirects to front end",
        ),
        400: OpenApiResponse(
            response=ErrorSerializer,
            description="Order Payment Status Error",
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
