from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
)

from .samples import (
    all_payments,
    single_payment,
    payment_id,
    make_payment_payload,
    tag_name,
)
from ..serializers import PaymentSerializer
from conf.core.serializers import ErrorSerializer
from conf.core.api.schema_extensons import (
    BaseSchema,
    session_q_params,
    reference_q_params,
)


ALL_PAYMENTS_SCHEMA = BaseSchema(
    operation_id="list payments",
    description="get all payments",
    tags=[tag_name],
    parameters=[
        session_q_params,
    ],
    responses={
        200: OpenApiResponse(
            response=PaymentSerializer,
            description="All Payments",
        ),
    },
    examples=[
        OpenApiExample(
            name="sample_request_data",
            value=all_payments,
            request_only=True,
        )
    ],
)

SINGLE_PAYMENT_SCHEMA = BaseSchema(
    operation_id="get payment",
    description="get a single payment",
    tags=[tag_name],
    parameters=[
        OpenApiParameter(
            name="id",
            description=payment_id,
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.PATH,
        ),
        session_q_params,
    ],
    responses={
        200: OpenApiResponse(
            response=PaymentSerializer,
            description="Single Payment",
        ),
    },
    examples=[
        OpenApiExample(
            name="sample_request_data",
            value=single_payment,
            request_only=True,
        )
    ],
)

CREATE_PAYMENT_URL_SCHEMA = BaseSchema(
    operation_id="create a payment url",
    description="create a payment url for an order and redirect to the payment url",
    tags=["Customer Orders"],
    parameters=[
        OpenApiParameter(
            name="id",
            description=payment_id,
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.PATH,
        ),
        session_q_params,
    ],
    responses={
        302: OpenApiResponse(
            #response=PaymentSerializer,
            description="Redirects to Payment service URL",
        ),
        400: OpenApiResponse(
            response=ErrorSerializer,
            description="Payment URL Failed",
        ),
    },
    examples=[
        OpenApiExample(
            name="sample_request_data",
            value=make_payment_payload,
            request_only=True,
        )
    ],
)
