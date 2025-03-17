from .base import SubscriptionEngine
from .free import FreeSubscription
from .basic import BasicSubscription
from .standard import StandardSubscription
from .premium import PremiumSubscription


def get_subscription_processor(subscription_type: str) -> SubscriptionEngine:
    processor = FreeSubscription
    if subscription_type == "basic":
        processor = BasicSubscription
    elif subscription_type == "premium":
        processor = PremiumSubscription
    elif subscription_type == "standard":
        processor = StandardSubscription
    return processor
