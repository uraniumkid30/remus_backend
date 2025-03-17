from typing import Any, Dict, Optional, Sequence, Union
from dataclasses import dataclass, asdict

from rest_framework.fields import empty
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiCallback,
    _SerializerType,
    _StrOrPromise,
    _SchemaType,
)


@dataclass
class BaseSchema:
    operation_id: Optional[str] = None
    parameters: Optional[Sequence[Union[OpenApiParameter, _SerializerType]]] = None
    request: Any = empty
    responses: Any = empty
    auth: Optional[Sequence[str]] = None
    description: Optional[_StrOrPromise] = None
    summary: Optional[_StrOrPromise] = None
    deprecated: Optional[bool] = None
    tags: Optional[Sequence[str]] = None
    filters: Optional[bool] = None
    exclude: Optional[bool] = None
    operation: Optional[_SchemaType] = None
    methods: Optional[Sequence[str]] = None
    versions: Optional[Sequence[str]] = None
    examples: Optional[Sequence[OpenApiExample]] = None
    extensions: Optional[Dict[str, Any]] = None
    callbacks: Optional[Sequence[OpenApiCallback]] = None
    external_docs: Optional[Union[Dict[str, str], str]] = None

    def to_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}


reference_id = "96009yniy"
session_id = "92b072d1-de3c-4a77-9126-b46f4d9fda76"


session_q_params = OpenApiParameter(
    "session",
    description="query params for session",
    required=True,
    location="query",
    examples=[
        OpenApiExample("session", value=session_id),
    ],
)

reference_q_params = OpenApiParameter(
    "reference",
    description="query params for reference",
    required=True,
    location="query",
    examples=[
        OpenApiExample("reference", value=reference_id),
    ],
)
