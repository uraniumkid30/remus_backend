from typing import Union, Tuple
from logging import Logger

from requests import request
import requests.exceptions as req_exceptions

from .exceptions import (
    UnExpectedStatusCode,
    TooManyRequests,
    NotFoundException,
    BadRequestException,
)
from .http import (
    Status,
    METHOD_EXPECTED_RESPONSE_CODE,
    HttpMethods,
)


APIResultType = Union[dict, list]


class BaseRequestClient:
    LOG_NAME: str = ""
    BASE_URL: str = ""
    APP_NAME: str = ""
    DATE_FORMAT = "%Y-%m-%d"
    MAX_RETRY = 5
    MAX_LIMIT = 50
    CALLS_PER_MINUTE = 200

    def __init__(self, *args, **kwargs):
        self.logger: Logger = self.get_logger(**kwargs)
        self.number_of_retrials = 0

    def set_base_url(self) -> str:
        """
        Updates and Returns the base url of Application api
        @return: str
        """
        raise NotImplementedError()

    def get_logger(self, **kwargs) -> Logger:
        """Get the logger to use here"""
        raise NotImplementedError()

    @staticmethod
    def raise_appropriate_exception_if_needed(response, expected_status_code=None):
        """
        Raises an appropriate exception for different status codes
        Exceptions may be used to handle the flow of code in callers.
        @raises: Exception
        """
        _status_code = int(response.status_code)
        if _status_code == Status.HTTP_400_BAD_REQUEST:
            raise BadRequestException(response.json())
        if _status_code == Status.HTTP_404_NOT_FOUND:
            raise NotFoundException(response.json())
        if _status_code == Status.HTTP_429_TOO_MANY_REQUESTS:
            raise TooManyRequests("Too many requests. Try sleeping for 1 minutes.")
        if expected_status_code:
            if _status_code not in expected_status_code:
                raise UnExpectedStatusCode(
                    f"Was expecting status code {expected_status_code}"
                    f"but I have received {_status_code}.\n"
                    f"{response.content}."
                )

    def _generate_params(self, raw_params={}) -> dict:
        """
        generates parameters from provided values
        """
        params = {}
        if isinstance(raw_params, dict):
            params.update(raw_params)
        return params

    def make_request(
        self,
        url: str,
        method: HttpMethods = HttpMethods.GET,
        extra_headers: dict = None,
        data=None,
        json_=None,
        params: dict = {},
        headers: dict = {},
        computed_url: str = "",
        raise_exceptions=True,
        auth=None,
    ) -> Tuple[int, APIResultType]:
        """
        Makes request to Client server for a url
        """
        try:
            response = request(
                method,
                url,
                headers=headers,
                data=data,
                json=json_,
                params=params,
                auth=auth,
            )
            self.header_response = response.headers
            status_code = response.status_code
            response_json = response.json()
        except (
            req_exceptions.ConnectionError,
            req_exceptions.ConnectTimeout,
        ) as err:
            print(f"{self.APP_NAME} Connection error {err}")
            raise_exceptions = False
            status_code = Status.HTTP_500_INTERNAL_SERVER_ERROR
            response_json = {"error": err}
            raise err
        except ValueError as el:
            print(f"ell {el}")
            response_json = {}
        except Exception as err:
            print(err)
            response_json = {}

        if raise_exceptions:
            _expected_status_code = (
                METHOD_EXPECTED_RESPONSE_CODE().data().get(method.upper())
            )
            self.raise_appropriate_exception_if_needed(response, _expected_status_code)

        return status_code, response_json

    def __retrieve(self, url: str = "", **kwargs) -> APIResultType:
        """
        Handles retrieval of resources, etc
        ** To retrieve by use of params is also available etc
        """

        raw_params = kwargs.get("params")
        computed_url = kwargs.get("computed_url")
        params = self._generate_params(raw_params)
        call_more_responses = True
        _data = []
        while call_more_responses:
            status_code, response_json = self.make_request(
                url, params=params, computed_url=computed_url
            )
            if self.is_resp_successful(status_code):
                if isinstance(response_json, dict):
                    call_more_responses = False
                    _data = [response_json or {}]
                elif isinstance(response_json, list):
                    data = response_json or []
                    _data.extend(data)
                    call_more_responses = False
                if not call_more_responses:
                    return _data
            else:
                return []
