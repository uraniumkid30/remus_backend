from abc import ABC, abstractmethod

from .schemas import ResponseSchema, DataSchema
from conf.core.types import DjangoModelType


class BaseResponse(ABC):
    @classmethod
    @abstractmethod
    def responses_data(cls, option: str = None, extra_data: dict = {}) -> DataSchema:
        """Defines all responses for a given view"""
        # be sure to use DataSchema and ResponseSchema
        pass

    @classmethod
    def responses(cls, option: str = None, extra_data: dict = {}) -> ResponseSchema:
        """Defines all responses for a given view"""
        return cls.compute_responses(option, extra_data)

    @classmethod
    def compute_responses(cls, option: str = None, extra_data: dict = {}):
        data: dict
        status: int
        data, status = cls.responses_data(option, extra_data)
        response: dict = {"data": DataSchema(**data), "status": status}
        return ResponseSchema(**response).to_dict()
