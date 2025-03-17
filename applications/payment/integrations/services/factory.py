from .paystack import PaystackService


def get_service(payment_service, data=None):
    service = PaystackService
    if payment_service == "paystack":
        pass
    return service(data)
