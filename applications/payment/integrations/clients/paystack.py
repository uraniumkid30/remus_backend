from django.conf import settings
from conf.core.request_client.base_client import (
    BaseRequestClient,
    HttpMethods,
    Status,
    APIResultType,
)
from conf.core.request_client.authenticators import TokenAuth


class PaystackAPI(BaseRequestClient):
    """
    Documentation: https://
    """

    APP_NAME = "Paystack"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.secret_key = settings.PAYSTACK_SECRET_KEY
        self.resource_name = "Paystack"
        self.auth_type = "Bearer"
        self.__authentication_token = self.secret_key
        self.set_base_url()

    def set_base_url(self) -> str:
        """
        Updates and Returns the base url of Application api
        @return: str
        """
        self.BASE_URL = "https://api.paystack.co"

    def get_logger(self, **kwargs):
        pass

    def make_request(
        self,
        url: str,
        method: str = HttpMethods.GET,
        extra_headers: dict = None,
        data=None,
        json_=None,
        params: dict = {},
        headers: dict = None,
        computed_url: str = "",
        raise_exceptions: bool = False,
        authenticate: bool = False,
    ) -> tuple:
        """
        Makes request to paystack server for a url
        """
        headers = headers or {}
        auth = self.compute_auth()
        full_url = f"{computed_url or self.BASE_URL}/{url}"

        if data is None:
            data = {}

        if extra_headers:
            headers.update(extra_headers)
        return super().make_request(
            full_url,
            method,
            extra_headers,
            data,
            json_,
            params,
            headers,
            computed_url,
            raise_exceptions,
            auth,
        )

    def compute_auth(self):
        return TokenAuth(
            **{
                "custom_header_data": {"token": self.__authentication_token},
                "auth_type": self.auth_type,
            }
        )

    def create_subaccount(self, request_payload: dict) -> APIResultType:
        url_path: str = "subaccount"
        status_code, response_json = self.make_request(
            url_path, method=HttpMethods.POST, json_=request_payload
        )
        if Status.is_success(status_code):
            result = response_json or []
            print("Subaccount successfully created")
        else:
            print("Couldnt Create subaccount ")
        return result

    def create_transaction(self, request_payload: dict) -> APIResultType:
        result = {}
        url_path: str = "charge"
        status_code, response_json = self.make_request(
            url_path, method=HttpMethods.POST, json_=request_payload
        )
        if Status.is_success(status_code):
            result = response_json or []
            print("Charge successfully created")
        else:
            print("Couldnt Create charge ")
        return result

    def initialize_web_transaction(self, request_payload: dict) -> APIResultType:
        result = {}
        url_path: str = "transaction/initialize"
        status_code, response_json = self.make_request(
            url_path, method=HttpMethods.POST, json_=request_payload
        )
        if Status.is_success(status_code):
            result = response_json or []
            print("Transaction successfully Initialized")
        else:
            print("Couldnt Initialize Transaction ")
        return result

    def verify_web_transaction(self, reference: str) -> APIResultType:
        result = {}
        url_path: str = f"transaction/verify/{reference}"
        status_code, response_json = self.make_request(url_path)
        if Status.is_success(status_code):
            result = response_json or []
            print("Transaction successfully Verified")
        else:
            print("Couldnt Verify Transaction ")
        return result
