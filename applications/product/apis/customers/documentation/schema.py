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
    r_category_tag_name,
)
from ..serializers import (
    ProductSerializer,
    RelatedCategorySerializer,
)
from conf.core.api.schema_extensons import BaseSchema, session_q_params


ALL_PRODUCTS_SCHEMA = BaseSchema(
    operation_id="list products",
    description="get all products",
    tags=[product_tag_name],
    parameters=[
        session_q_params,
    ],
    responses={
        200: OpenApiResponse(
            response=ProductSerializer,
            description="All Products",
        ),
    },
    examples=[
        OpenApiExample(
            name="sample_request_data",
            value=all_products,
            response_only=True,
        )
    ],
)

SINGLE_PRODUCT_SCHEMA = BaseSchema(
    operation_id="get product",
    description="get a single product",
    tags=[product_tag_name],
    parameters=[
        OpenApiParameter(
            name="id",
            description=product_id,
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.PATH,
        ),
        session_q_params,
    ],
    responses={
        200: OpenApiResponse(
            response=ProductSerializer,
            description="Single Product",
        ),
    },
    examples=[
        OpenApiExample(
            name="sample_request_data",
            value=single_product,
            response_only=True,
        )
    ],
)


ALL_PRODUCTS_SCHEMA = BaseSchema(
    operation_id="list products",
    description="get all products",
    tags=[product_tag_name],
    parameters=[
        session_q_params,
    ],
    responses={
        200: OpenApiResponse(
            response=ProductSerializer,
            description="All Products",
        ),
    },
    examples=[
        OpenApiExample(
            name="sample_request_data",
            value=all_products,
            response_only=True,
        )
    ],
)

SINGLE_CATEGORY_SCHEMA = BaseSchema(
    operation_id="get product category",
    description="get a single product category",
    tags=[category_tag_name],
    parameters=[
        OpenApiParameter(
            name="id",
            description=category_id,
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.PATH,
        ),
        session_q_params,
    ],
    responses={
        200: OpenApiResponse(
            response=RelatedCategorySerializer,
            description="Single Product Category",
        ),
    },
    examples=[
        OpenApiExample(
            name="sample_request_data",
            value=single_category,
            response_only=True,
        )
    ],
)

ALL_CATEGORY_SCHEMA = BaseSchema(
    operation_id="list product categories",
    description="get all product categories",
    tags=[category_tag_name],
    parameters=[
        session_q_params,
    ],
    responses={
        200: OpenApiResponse(
            response=RelatedCategorySerializer,
            description="All Product Categories",
        ),
    },
    examples=[
        OpenApiExample(
            name="sample_request_data",
            value=all_categories,
            response_only=True,
        )
    ],
)

SINGLE_RCATEGORY_SCHEMA = BaseSchema(
    operation_id="get restaurant product category",
    description="get a single restaurant product category",
    tags=[r_category_tag_name],
    parameters=[
        OpenApiParameter(
            name="restaurant_id",
            description="id of the restaurant",
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.PATH,
        ),
        OpenApiParameter(
            name="id",
            description="id of the category",
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.PATH,
        ),
        session_q_params,
    ],
    responses={
        200: OpenApiResponse(
            response=RelatedCategorySerializer,
            description="Single Product Category",
        ),
    },
    examples=[
        OpenApiExample(
            name="sample_response_data",
            value=single_category,
            response_only=True,
        )
    ],
)

ALL_RCATEGORY_SCHEMA = BaseSchema(
    operation_id="list restaurant product categories",
    description="get all restaurant product categories",
    tags=[r_category_tag_name],
    parameters=[
        OpenApiParameter(
            name="restaurant_id",
            description="id of the restaurant",
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.PATH,
        ),
        session_q_params,
    ],
    responses={
        200: OpenApiResponse(
            response=RelatedCategorySerializer,
            description="All Product Categories",
        ),
    },
    examples=[
        OpenApiExample(
            name="sample_response_data",
            value=all_categories,
            response_only=True,
        )
    ],
)
