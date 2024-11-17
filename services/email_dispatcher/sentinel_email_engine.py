from django.conf import settings
from django.core.mail import send_mail as django_send_mail

from .base_engine import EmailEngine
from conf.core.request_client.base_client import (
    BaseRequestClient,
    HttpMethods
)


class SentinelEmailClient(BaseRequestClient):
    def set_base_url(self) -> str:
        """
        Updates and Returns the base url of Application api
        @return: str
        """
        return 'https://api.sendinblue.com/v3/smtp/email'

    def get_logger(self, **kwargs):
        """Get the logger to use here"""
        pass

    def send_mail(self, email_data):
        url = ""
        method = HttpMethods.POST
        extra_headers = {"api_key": settings.SENTINEL_API_KEY}
        self.make_request(
            url=url,
            method=method,
            extra_headers=extra_headers
        )


class SentinelEmailEngine(EmailEngine):
    @classmethod
    def get_configuration(cls):
        configurations: dict = {}
        return configurations

    @classmethod
    def get_email_sending_parameters(
        cls, to_email: str, from_email: str = "", **kwargs
    ) -> dict:
        sender = {
            "email": from_email or cls.FROM_EMAIL
        }
        to = {
            "email": to_email
        }
        body = kwargs.get("body")
        subject = kwargs.get("subject")
        if kwargs.get("sender_name"):
            sender["name"] = kwargs.get("sender_name")
        if kwargs.get("to_name"):
            to["name"] = kwargs.get("to_name")
        email_parameters = {
            "sender": sender,
            "to": [
                to
            ],

            "htmlContent": body,
            "subject": subject
        }
        return email_parameters

    @classmethod
    def __send_mail(cls, to_email: str, from_email: str = "", **kwargs):
        email_parameters = cls.get_email_sending_parameters(
            to_email, from_email, **kwargs
        )
        try:
            client = SentinelEmailClient()
            client.send_mail(**email_parameters)
        except Exception as Err:
            print(f"Email Sending Error {Err}")
        else:
            print("Email Sent")
