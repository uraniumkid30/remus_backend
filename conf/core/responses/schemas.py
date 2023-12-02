from typing import Any

from ..base_dataclasses import BaseSchema, dataclass

@dataclass
class DataSchema(BaseSchema):
    code: str = "00"
    message: Any = None

@dataclass
class ResponseSchema(BaseSchema):
    data: DataSchema = None
    status: int = 200
