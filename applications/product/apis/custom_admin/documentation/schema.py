from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
)

from .samples import (
    all_products,
    single_product,
    product_id,
    product_tag_name,
    all_categories,
    single_category,
    category_id,
    category_tag_name,
)
from ..serializers import AdminProductSerializer, RelatedProductSerializer
from conf.core.api.schema_extensons import BaseSchema, session_q_params


ALL_PRODUCTS_SCHEMA = BaseSchema(
    operation_id="list admin products",
    description="get all admin products",
    tags=[product_tag_name],
    responses={
        200: OpenApiResponse(
            response=AdminProductSerializer,
            description="All Products",
        ),
    },
    examples=[
        OpenApiExample(
            name="sample_request_data",
            value=all_products,
            request_only=True,
        )
    ],
)

SINGLE_PRODUCT_SCHEMA = BaseSchema(
    operation_id="get admin product",
    description="get a single admin product",
    tags=[product_tag_name],
    parameters=[
        OpenApiParameter(
            name="id",
            description=product_id,
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.PATH,
        ),
    ],
    responses={
        200: OpenApiResponse(
            response=AdminProductSerializer,
            description="Single Product",
        ),
    },
    examples=[
        OpenApiExample(
            name="sample_request_data",
            value=single_product,
            request_only=True,
        )
    ],
)


ALL_PRODUCTS_SCHEMA = BaseSchema(
    operation_id="list admin products",
    description="get all admin products",
    tags=[product_tag_name],
    responses={
        200: OpenApiResponse(
            response=AdminProductSerializer,
            description="All Products",
        ),
    },
    examples=[
        OpenApiExample(
            name="sample_request_data",
            value=all_products,
            request_only=True,
        )
    ],
)

SINGLE_CATEGORY_SCHEMA = BaseSchema(
    operation_id="get admin product category",
    description="get a single admin product category",
    tags=[category_tag_name],
    parameters=[
        OpenApiParameter(
            name="id",
            description=category_id,
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.PATH,
        ),
    ],
    responses={
        200: OpenApiResponse(
            response=RelatedProductSerializer,
            description="Single Product Category",
        ),
    },
    examples=[
        OpenApiExample(
            name="sample_request_data",
            value=single_category,
            request_only=True,
        )
    ],
)

ALL_CATEGORY_SCHEMA = BaseSchema(
    operation_id="list admin product categories",
    description="get all admin product categories",
    tags=[category_tag_name],
    parameters=[
        session_q_params,
    ],
    responses={
        200: OpenApiResponse(
            response=RelatedProductSerializer,
            description="All Product Categories",
        ),
    },
    examples=[
        OpenApiExample(
            name="sample_request_data",
            value=all_categories,
            request_only=True,
        )
    ],
)