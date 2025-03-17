from datetime import timedelta, datetime

from django.dispatch import receiver
from django.db.models.signals import post_save
from applications.merchant.models import (
    Subscription,
    SubscriptionPayment,
    BankDetail,
)


@receiver(post_save, sender=Subscription)
def create_subscription_payment(sender, instance, created: bool, **kwargs):
    if created and instance:
        first_payment = None
        next_payment = None
        for item in range(1, instance.contract_length + 1):
            duration = item * instance.get_cycle_days()
            expires_at = instance.contract_start_date + timedelta(days=duration)
            payment_date = None
            status = "unpaid"
            if instance.category == "free":
                payment_date = datetime.now()
                status = "paid"
            sub_payment = SubscriptionPayment.objects.create(
                expires_at=expires_at,
                subscription=instance,
                amount=instance.billing_price,
                payment_date=payment_date,
                status=status,
                currency=instance.currency
            )
            if item == 1:
                first_payment = sub_payment.id
            if item == 2:
                next_payment = sub_payment.id
        instance.current_payment = first_payment
        instance.next_payment = next_payment
        instance.save()


@receiver(post_save, sender=Subscription)
def create_restaurant_bank_info(sender, instance, created: bool, **kwargs):
    if created and instance:
        BankDetail.objects.create(restaurant=instance.restaurant)
