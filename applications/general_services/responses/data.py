from typing import Tuple

from rest_framework import status

from conf.core.responses.base import (
    BaseResponse,
    ResponseSchema, DataSchema,
)
from conf.core.responses.decorators import enhance_parameters


class EmailViewResponses(BaseResponse):
    EMAIL_SENT = "EMAIL_SENT"

    @classmethod
    @enhance_parameters
    def responses_data(cls, option: str=None, extra_data: dict={}) -> Tuple[DataSchema,int]:
        if option == cls.EMAIL_SENT:
            data = {
                'code': '00',
                'message': "email successfully sent."
            }
            http_status = status.HTTP_200_OK
        else:
            data = {
                'message': "Invalid details",
                "code": "33"
            }
            http_status = status.HTTP_400_BAD_REQUEST
        return data, http_status
