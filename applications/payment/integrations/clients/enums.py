from dataclasses import dataclass


@dataclass
class PAYSTACK_DEFAULT_RESPONSE:
    status: bool
    message: str
    data: dict


@dataclass
class PAYSTACK_SUBACCOUNT_PAYLOAD:
    business_name: str
    bank_code: str
    account_number: str
    percentage_charge: str


@dataclass
class PAYSTACK_TRANSACTION_PAYLOAD:
    email: str
    amount: str
    subaccount: str = ""
    transaction_charge: str = ""
    bearer: str = ""


@dataclass
class PAYSTACK_CHARGE_TRANSFER_PAYLOAD:
    email: str
    amount: str
    bank_transfer: dict = {
        "account_expires_at": "2023-09-12T13:10:00Z"
    }

"""
"currency": "NGN",
      "qr": {
        "provider" : "visa"
      }
    "last4":"4081",
  "trans":"4511462450",
  "offset": "-60",
  "remember_card": false
"""