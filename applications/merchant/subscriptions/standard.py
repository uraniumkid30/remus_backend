from .base import SubscriptionEngine


class StandardSubscription(SubscriptionEngine):
    def can_send_sms(self) -> bool:
        return True

    def can_send_whatsapp(self) -> bool:
        return False

    def can_send_email(self) -> bool:
        return True

    def can_send_generate_report(self) -> bool:
        return True

    def can_send_generate_receipt(self) -> bool:
        return True
