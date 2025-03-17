from abc import ABC, abstractmethod
from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel

from applications.administrator.models import RunningCost
from services.currency_exchange import WiseAPIClient


class PricingSchema(BaseModel):
    category: str
    intial_price: Decimal
    price_per_table: Decimal
    billing_price: Decimal
    billing_cycle: str
    order_volume: str
    percent_per_order: float
    charge: Decimal
    service_charge: Decimal


class SubscriptionSchema(BaseModel):
    id: str
    restaurant_id: str
    category: str
    billing_cycle: str
    status: str
    meta: dict
    billing_price: Decimal
    total_price: Decimal
    number_of_tables: int

    billing_count: int
    auto_renew: bool
    contract_length: int

    date_cancelled: datetime
    contract_start_date: datetime
    contract_end_date: datetime
    next_billing_date: datetime


class SubscriptionEngine(ABC):
    """Interface for all solid implementations"""

    def __init__(
        self,
        subscription_pricing: PricingSchema,
        subscription: SubscriptionSchema = None,
    ):
        self.subscription_pricing = subscription_pricing
        self.subscription = subscription
        self.default_currency = self.subscription_pricing.currency
        self.destination_currency = self.subscription.currency
        exchange_client = WiseAPIClient()
        if self.default_currency == self.destination_currency:
            self.rate = 1
        else:
            try:
                rate: dict = exchange_client.get_rates(
                    {
                        "source": self.default_currency,
                        "target": self.destination_currency,
                    }
                )
                self.rate = rate.get("rate")
            except:
                self.rate = 1

    @abstractmethod
    def can_send_sms(self) -> bool:
        pass

    @abstractmethod
    def can_send_whatsapp(self) -> bool:
        pass

    @abstractmethod
    def can_send_email(self) -> bool:
        pass

    @abstractmethod
    def can_send_generate_report(self) -> bool:
        pass

    @abstractmethod
    def can_send_generate_receipt(self) -> bool:
        pass

    @classmethod
    def get_running_cost(cls, duration: str) -> float:
        all_running_cost = RunningCost.objects.all()
        total_running_cost = 0
        for item in all_running_cost:
            total_running_cost += item.monthly_fee
        if duration == "yearly":
            total_running_cost * 12
        return total_running_cost

    def convert_rate(self, amount: float) -> float:
        return round(float(amount) * self.rate, 2)

    def calculate_billing_price(self) -> float:
        """Calculates total"""
        return sum(
            [
                self.convert_rate(self.subscription_pricing.charge),
                self.convert_rate(self.subscription_pricing.service_charge),
            ]
        )

    def get_total(self):
        """Calculates total"""
        tech_price = self.convert_rate(self.subscription_pricing.intial_price)
        unit_table_price = self.convert_rate(
            self.subscription_pricing.price_per_table
        )
        number_of_tables = self.subscription.number_of_tables
        total_table_price = number_of_tables * unit_table_price
        billing_cost = self.convert_rate(self.subscription.billing_price)
        return sum([tech_price, total_table_price, billing_cost])

    def construct_meta_data(self) -> dict:
        intial_price = self.convert_rate(
            self.subscription_pricing.intial_price
        )
        charge = self.convert_rate(self.subscription_pricing.charge)
        service_charge = self.convert_rate(
            self.subscription_pricing.service_charge
        )
        price_per_table = self.convert_rate(
            self.subscription_pricing.price_per_table
        )
        billing_price = self.convert_rate(
            self.subscription_pricing.billing_price
        )
        return {
            "id": str(self.subscription_pricing.id),
            "category": self.subscription_pricing.category,
            "intial_price": intial_price,
            "charge": charge,
            "service_charge": service_charge,
            "price_per_table": price_per_table,
            "billing_price": billing_price,
            "billing_cycle": self.subscription_pricing.billing_cycle,
            "order_volume": self.subscription_pricing.order_volume,
            "percent_per_order": self.subscription_pricing.percent_per_order,
        }
