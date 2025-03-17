from datetime import datetime

from rest_framework import serializers
from django.template.loader import render_to_string


from conf.core.serializers import EXCLUDED_TIME_FIELDS
from applications.payment.models import Payment, Receipt
from applications.payment.enums import get_meta
from applications.accounts.models import Customer
from applications.merchant.models import Subscription, BankDetail
from applications.order.apis.customers.serializers import ReadOrderSerializer
from services.email_dispatcher import email_engine_factory
from applications.payment.integrations.services.factory import get_service
from services.cloud.aws.utils import get_file_url


class PaymentSerializer(serializers.ModelSerializer):
    order = ReadOrderSerializer(read_only=True)

    class Meta:
        model = Payment
        exclude = [*EXCLUDED_TIME_FIELDS]


class WritePaymentSerializer(serializers.ModelSerializer):
    def validate(self, data):
        order = data["order"]
        if order.total != data["amount_paid"]:
            raise serializers.ValidationError("wrong payment amount")
        if not isinstance(data["payment_method_meta"], dict):
            raise serializers.ValidationError("meta needs to be an object")
        meta = get_meta(data["payment_method"])
        try:
            meta(**data["payment_method_meta"])
        except:
            raise serializers.ValidationError(meta.errors())
        return data

    class Meta:
        model = Payment
        fields = "__all__"
        extra_kwargs = {
            "order": {"required": True},
            "payment_method": {"required": True},
            "payment_method_meta": {"required": True},
            "amount_paid": {"required": True},
            "currency": {"required": True},
            "id": {"read_only": True},
        }

    def create(self, validated_data):
        order = validated_data["order"]
        restaurant_record = order.table.restaurant
        customer = Customer.objects.get(orders=order)
        customer = {"name": customer.get_full_name(), "email": customer.email}
        try:
            res = self.send_money(
                customer["email"],
                validated_data,
                restaurant_record,
            )
            data = res.get("data", {})
            status = data.get("status")
            validated_data["status"] = status
            validated_data["payment_id"] = data.get("reference")
            validated_data["merchant_amount"] = res.get("merchant_amount")
            validated_data["operator_amount"] = res.get("owner_amount")
            order.payment_status = status
            order.save()
            payment = Payment.objects.create(**validated_data)
            if status == "success":
                receipt = Receipt.objects.create(payment=payment)
                receipt_link, receipt_name = self.get_receipt_url(receipt)
                self.notify_customer(
                    payment,
                    receipt_name,
                    receipt_link,
                    customer,
                )
            return payment
        except Exception as e:
            print(e)
            raise ValueError("I could not process payment")

    def notify_customer(
        self,
        payment: Payment,
        receipt_file_name: str,
        receipt_link: str,
        customer: dict,
    ):
        restaurant_record = payment.order.table.restaurant
        restaurant_name = restaurant_record.name
        restaurant_email = restaurant_record.email or "receipts@donotreply.com"
        receiver = [
            {
                "name": customer["name"],
                "email": customer["email"],
            }
        ]
        logo_url = get_file_url(restaurant_record.logo.name)
        body = render_to_string(
            "order_payment_email.html",
            {
                "logo_url": logo_url,
                "customer_name": customer["name"],
                "order_number": payment.order.order_number,
            },
        )
        attachments = [
            {
                "url": receipt_link,
                "name": receipt_file_name,
            }
        ]
        data = {
            "body": body,
            "subject": f"Payment Receipt {str(datetime.today().date())}",
            "sender_name": restaurant_name,
            "attachments": attachments,
        }
        to = receiver
        _from = restaurant_email
        cl = email_engine_factory("sentinel")
        cl.send_mail(to, _from, **data)

    def get_receipt_url(self, receipt):
        url = receipt.pdf_document.name
        return (
            get_file_url(url),
            url.split("/")[-1],
        )

    def send_money(self, customer_email, validated_data, restaurant_record):
        sub = Subscription.objects.get(restaurant=restaurant_record)
        bank_detail = BankDetail.objects.get(restaurant=restaurant_record)
        percent_per_order = sub.billing_price.percent_per_order
        our_amount = validated_data["amount_paid"] * percent_per_order
        merchant_amount = validated_data["amount_paid"] - our_amount
        service = get_service(self.payment_provider)
        data = service.send_money(
            customer_email,
            validated_data,
            bank_detail,
        )
        return {
            "data": data,
            "owner_amount": our_amount,
            "merchant_amount": merchant_amount,
        }
