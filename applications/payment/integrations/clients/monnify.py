import base64
import hashlib
from datetime import datetime, timedelta

from django.conf import settings
from conf.core.request_client.base_client import (
    BaseRequestClient,
    HttpMethods,
    Status,
    APIResultType,
)
from conf.core.request_client.authenticators import TokenAuth


class MonnifyAPI(BaseRequestClient):
    """
    Documentation: https://
    """

    APP_NAME = "Monnify"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.monnify_secret_key = settings.MONNIFY_SECRET_KEY
        self.resource_name = "Monnify"
        self.__authentication_token = ""
        self.expires_at = None
        self.auth_type = "Bearer"
        self.set_base_url()

    def set_base_url(self) -> str:
        """
        Updates and Returns the base url of Application api
        @return: str
        """
        MONNIFY_URL_PREFIX = settings.MONNIFY_BASEURL_PREFIX
        self.BASE_URL = MONNIFY_URL_PREFIX + "monnify.com/api/v1"

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
        raise_exceptions: bool = True,
        authenticate: bool = False,
    ) -> tuple:
        """
        Makes request to Monnify server for a url
        """
        headers = headers or {}
        if self.token_is_expired() and authenticate is False:
            self.refresh_token()
        elif self.token_is_expired() and authenticate is True:
            self.auth_type = "Bearer"
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

    def clear_hash(self):
        self.hash_text = ""

    def hashKey(self, **kwargs):
        client_secret = kwargs["clientSecret"]
        paymentReference = kwargs["paymentReference"]
        amountPaid = kwargs["amountPaid"]
        paidOn = kwargs["paidOn"]
        transactionReference = kwargs["transactionReference"]
        data = (
            client_secret,
            paymentReference,
            amountPaid,
            paidOn,
            transactionReference,
        )
        text = "|".join(data)
        byte_text = bytes(text, "utf8")
        hashtext = hashlib.sha512(byte_text).hexdigest()
        return hashtext

    def get_encoded_token(self):
        text = f"{settings.MONNIFY_API_KEY}:{self.monnify_secret_key}"
        byte_text = bytes(text, "utf8")
        encoded = base64.b64encode(byte_text)
        return encoded.decode()

    def token_is_expired(self) -> bool:
        verdict = True
        if self.expires_at is not None and datetime.now() > self.expires_at:
            return verdict
        elif self.expires_at is None:
            return verdict
        else:
            verdict = False
            return verdict

    def compare_hash(
        self,
        hash_data,
        transaction_hash,
    ):
        hash_data.update(
            {
                "clientSecret": self.monnify_secret_key,
            }
        )
        self.clear_hash()
        self.hash_text = self.hashKey(**hash_data)
        self.hash_text_ok = self.hash_text == transaction_hash

    def refresh_token(self, **kwargs):
        url_path = "auth/login"
        self.__authentication_token = self.get_encoded_token()
        self.auth_type = "Basic"
        status_code, response_json = self.make_request(
            url_path, method=HttpMethods.POST, json_={}, authenticate=True
        )
        if Status.is_success(status_code):
            body: dict = response_json["responseBody"]
            self.__authentication_token = body["accessToken"]
            duration: int = body["expiresIn"]
            self.expires_at = datetime.now() + timedelta(seconds=duration)
            self.logger.info("Token Generated Successfully")
        else:
            self.logger.info("Couldnt Generate new Token")

    def reserve_account(self, request_payload: dict) -> APIResultType:
        url_path: str = "bank-transfer/reserved-accounts"
        request_payload.update(
            {
                "currencyCode": settings.MONNIFY_CURRENCY_CODE,
                "contractCode": settings.MONNIFY_CONTRACT_CODE,
            }
        )
        status_code, response_json = self.make_request(
            url_path, method=HttpMethods.POST, json_=request_payload
        )
        if Status.is_success(status_code):
            result = response_json or []
            self.logger.info("Reserved account successfully")
        else:
            self.logger.info("Couldnt Reserved account ")
        return result

    def get_transactions(self, request_data):
        url_path = "merchant/transactions/query"
        status_code, response_json = self.make_request(url_path, params=request_data)
        if Status.is_success(status_code):
            result = response_json or []
            self.logger.info("Fetched Transactions successfully")
        else:
            self.logger.info("Couldnt Fetched Transactions ")
        return result
