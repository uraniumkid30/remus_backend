from dataclasses import dataclass

from .base import PaymentService
from applications.payment.enums import PaymentMethod
from applications.payment.integrations.clients.paystack import PaystackAPI


@dataclass
class AccountData:
    account_name: str
    bank_code: str
    account_number: str
    restaurant_name: str


class PaystackService(PaymentService):
    def get_client(self) -> PaystackAPI:
        return PaystackAPI()

    def create_account_id(self, subscription, data: dict):
        account_data: AccountData = AccountData(**data)
        percent_order = subscription.billing_price.percent_per_order
        payload = {
            "business_name": subscription.name or account_data.account_name,
            "settlement_bank": account_data.bank_code,
            "account_number": account_data.account_number,
            "percentage_charge": float(percent_order),
        }
        res = self.client.create_subaccount(payload)
        if res["status"] is False:
            print(res["message"])
            return ""
        else:
            return res.get("data", {}).get("subaccount_code", "")

    def send_money(
        self,
        customer_email: str,
        data: dict,
        bank_detail=None,
    ):
        payload = {
            "email": customer_email,
            "amount": str(float(data["amount_paid"]) * 100),
            "card": data["payment_method_meta"],
        }
        if bank_detail:
            payload["subaccount"] = bank_detail.account_id
        return self.client.create_transaction(payload).get("data", {})

    def create_payment_link(
        self,
        customer_email: str,
        data: dict,
        bank_detail=None,
    ):
        payload = {
            "email": customer_email,
            "amount": str(float(data["amount_to_pay"]) * 100),
            "callback_url": data["callback_url"],
            "channels": PaymentMethod.supported_channels()
        }
        if bank_detail:
            payload["subaccount"] = bank_detail.account_id
        return self.client.initialize_web_transaction(payload).get("data", {})

    def verify_payment(
        self,
        reference: str,
    ):
        return self.client.verify_web_transaction(reference).get("data", {})
