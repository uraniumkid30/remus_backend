from typing import Tuple, Any, Hashable
from abc import ABC, abstractmethod
from django.db.models.fields import PositiveSmallIntegerField


class CustomEnum(ABC):
    class Enum(object):
        name = None
        value = None
        type = None

        def __init__(self, name, value, type):
            self.key = name
            self.name = name
            self.value = value
            self.type = type

        def __str__(self):
            return self.name

        def __repr__(self):
            return self.name

        def __eq__(self, other):
            if other is None:
                return False
            if isinstance(other, CustomEnum.Enum):
                return self.value == other.value
            raise TypeError

    @classmethod
    def choices(c):
        attrs = [a for a in c.__dict__.keys() if a.isupper()]
        values = [
            (c.__dict__[v], CustomEnum.Enum(v, c.__dict__[v], c).__str__())
            for v in attrs
        ]
        return sorted(values, key=lambda x: x[0])

    @classmethod
    @abstractmethod
    def default(cls):
        """
        Returns default value, which is the first one by default.
        Override this method if you need another default value.
        """
        return cls.choices()[0][0]

    @classmethod
    def field(cls, **kwargs):
        """
        A shortcut for
        Usage:
            class MyModelStatuses(CustomEnum):
                UNKNOWN = 0
            class MyModel(Model):
                status = MyModelStatuses.field(label='my status')
        """
        field = PositiveSmallIntegerField(
            choices=cls.choices(), default=cls.default(), **kwargs
        )
        field.enum = cls
        return field

    @classmethod
    def get(c, value):
        if type(value) is int:
            try:
                return [
                    CustomEnum.Enum(k, v, c)
                    for k, v in c.__dict__.items()
                    if k.isupper() and v == value
                ][0]
            except Exception:
                return None
        else:
            try:
                key = value.upper()
                return CustomEnum.Enum(key, c.__dict__[key], c)
            except Exception:
                return None

    @classmethod
    def key(c, key):
        try:
            return [value for name, value in c.__dict__.items() if name == key.upper()][
                0
            ]
        except Exception:
            return None

    @classmethod
    def name(c, key):
        try:
            return [name for name, value in c.__dict__.items() if value == key][0]
        except Exception:
            return None

    @classmethod
    def get_counter(c) -> dict:
        counter = {}
        for key, value in c.__dict__.items():
            if key.isupper():
                counter[value] = 0
        return counter

    @classmethod
    def items(c) -> list:
        attrs = [a for a in c.__dict__.keys() if a.isupper()]
        values = [(v, c.__dict__[v]) for v in attrs]
        return sorted(values, key=lambda x: x[1])

    @classmethod
    def is_valid_transition(c, from_status, to_status) -> bool:
        return from_status == to_status or from_status in c.transition_origins(
            to_status
        )

    @classmethod
    def transition_origins(c, to_status):
        return c._transitions[to_status]

    @classmethod
    def get_name(c, key: Hashable) -> Any:
        choices_name = dict(c.choices())
        return choices_name.get(key)


class PricingCurrency(CustomEnum):
    DOLLAR = "USD"

    @classmethod
    def choices(cls) -> Tuple[Tuple[str, str]]:
        return (
            (cls.DOLLAR, cls.DOLLAR),
        )

    @classmethod
    def get_symbol(cls, currency: str):
        data = {
            cls.DOLLAR: "$",
        }
        return data[currency]

    @classmethod
    def default(cls):
        return cls.DOLLAR


class Currency(CustomEnum):
    NAIRA = "NGN"
    DOLLAR = "USD"
    EURO = "EUR"
    UGANDA_SHILLINGS = "UGX"

    @classmethod
    def choices(cls) -> Tuple[Tuple[str, str]]:
        return (
            (cls.NAIRA, cls.NAIRA),
            (cls.DOLLAR, cls.DOLLAR),
            (cls.EURO, cls.EURO),
        )

    @classmethod
    def get_symbol(cls, currency: str):
        data = {
            cls.NAIRA: "₦",
            cls.DOLLAR: "$",
            cls.EURO: "€",
            cls.UGANDA_SHILLINGS: "UGX"
        }
        return data[currency]

    @classmethod
    def default(cls):
        return cls.NAIRA


class PaymentOption(CustomEnum):
    UNPAID = "unpaid"
    PAID = "paid"

    @classmethod
    def choices(cls) -> Tuple[Tuple[str, str]]:
        return (
            (cls.PAID, cls.PAID.capitalize()),
            (cls.UNPAID, cls.UNPAID.capitalize()),
        )

    @classmethod
    def default(cls):
        return cls.UNPAID


class PaymentStatus(CustomEnum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"

    @classmethod
    def choices(cls) -> Tuple[Tuple[str, str]]:
        return (
            (cls.PENDING, "PENDING"),
            (cls.SUCCESS, "SUCCESS"),
            (cls.FAILED, "FAILED"),
        )

    @classmethod
    def default(cls):
        return cls.PENDING
