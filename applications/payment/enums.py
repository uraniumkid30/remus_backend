from dataclasses import dataclass, asdict

from conf.core.enums import CustomEnum


class PaymentMethod(CustomEnum):
    CARD = "card"
    BANK = "bank"
    BANK_TRANSFER = "bank_transfer"

    @classmethod
    def choices(cls):
        return (
            (cls.CARD, cls.CARD.upper()),
            (cls.BANK, cls.BANK.upper()),
            (cls.BANK_TRANSFER, cls.BANK_TRANSFER.upper()),
        )

    @classmethod
    def default(cls):
        return cls.CARD
    
    @classmethod
    def supported_channels(cls):
        return [cls.CARD]


@dataclass
class CardMeta:
    number: str
    cvv: int
    expiry_month: int
    expiry_year: int

    def to_dict(self):
        return {k: v for k, v in asdict(self).items()}

    @classmethod
    def errors(cls):
        data = "number(str), cvv(int), expiry_month(int), expiry_year(int)"
        return [f"Required fields are CARD PAYMENT {data}"]


def get_meta(payment_method, payment_provider: str = None):
    if payment_method == PaymentMethod.CARD:
        return CardMeta
