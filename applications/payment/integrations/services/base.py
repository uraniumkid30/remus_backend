from abc import ABC, abstractmethod


class PaymentService(ABC):
    def __init__(self, client_params: dict):
        self.client_params = client_params
        self.client = self.get_client()

    @abstractmethod
    def create_account_id(self):
        pass

    @abstractmethod
    def get_client(self):
        pass

    @abstractmethod
    def send_money(
        self,
        subscription,
        data: dict,
        bank_detail=None,
    ):
        pass

    @abstractmethod
    def create_payment_link(
        self,
        customer_email: str,
        data: dict,
        bank_detail=None,
    ):
        pass

    @abstractmethod
    def verify_payment(
        self,
        reference: str,
    ):
        pass
