from applications.merchant.models import (
    Subscription,
    SubscriptionPayment,
)


def is_subscription_active(_filter: dict):
    try:
        sub = Subscription.objects.get(**_filter)
        sub_payment = SubscriptionPayment.objects.get(id=sub.current_payment)
        is_expired = sub.is_expired() or sub_payment.is_expired()
        bad_status = sub_payment.status == "unpaid" or sub.status != "active"
        return not (is_expired or bad_status)
    except SubscriptionPayment.DoesNotExist:
        return False
    except Subscription.DoesNotExist:
        return False