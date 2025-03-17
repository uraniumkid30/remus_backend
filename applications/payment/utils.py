from datetime import datetime
from decimal import Decimal

from django.urls import reverse
from django.template.loader import render_to_string

from applications.payment.models import Payment, Receipt
from applications.accounts.models import Customer
from applications.merchant.models import Subscription, BankDetail
from services.email_dispatcher import email_engine_factory
from applications.payment.integrations.services.factory import get_service
from services.cloud.aws.utils import get_file_url
from applications.order.models import Order


class PaymentHandler:
    def __init__(self, order_id, session_id):
        try:
            self.session_id = session_id
            self.order = Order.objects.get(pk=order_id)
            self.restaurant = self.order.table.restaurant
            self.bank_detail = BankDetail.objects.get(
                restaurant=self.restaurant,
            )
            self.sub = Subscription.objects.get(restaurant=self.restaurant)
            customer = Customer.objects.get(orders=self.order)
            self.customer_data = {
                "name": customer.get_full_name(),
                "email": customer.email,
            }
            self.payment_service = get_service(self.sub.payment_provider)
        except Exception as err:
            raise err

    def get_redirect_url(self, session_id):
        backend = self.restaurant.platform_setting.api_domain
        url_name: str = "customer_applications:order:orders-payment-redirect"
        session = f"?session={session_id}"
        return backend + reverse(url_name, args=[str(self.order.id)]) + session

    def create_payment(self, reference):
        try:
            response = self.payment_service.verify_payment(reference)
            status = response.get("status") or "pending"
            percent_per_order = self.sub.subscription_price.percent_per_order
            operator_amount = self.order.total * Decimal(percent_per_order)
            merchant_amount = self.order.total - operator_amount
            data = {
                "order": self.order,
                "status": status,
                "payment_id": reference,
                "merchant_amount": merchant_amount,
                "operator_amount": operator_amount,
            }
            self.order.payment_status = status
            self.order.save()

            payment_record = Payment.objects.filter(order=self.order)
            if payment_record.exists():
                payment = payment_record.last()
            else:
                print("payment_created")
                payment = Payment.objects.create(**data)
            if status != "success":
                raise
            payment.payment_method = response["authorization"]["channel"]
            payment.save()
            receipt = Receipt.objects.create(payment=payment)
            receipt_link, receipt_name = self.get_receipt_url(receipt)
            self.notify_customer(
                receipt_name,
                receipt_link,
            )
            return payment
        except Exception as e:
            print(e)
            raise ValueError("I could not process payment")

    def notify_customer(
        self,
        receipt_file_name: str,
        receipt_link: str,
    ):
        restaurant_name = self.restaurant.name
        restaurant_email = self.restaurant.email or "receipts@donotreply.com"
        receiver = [self.customer_data]
        logo_url = get_file_url(self.restaurant.logo.name)
        body = render_to_string(
            "order_payment_email.html",
            {
                "logo_url": logo_url,
                "customer_name": self.customer_data["name"],
                "order_number": self.order.order_number,
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

    def create_checkout_url(
        self,
    ):
        try:
            url = self.get_redirect_url(self.session_id)
            payload = {
                "callback_url": url,
                "amount_to_pay": self.order.total,
            }

            data = self.payment_service.create_payment_link(
                self.customer_data["email"],
                payload,
                self.bank_detail,
            )
            return data["authorization_url"]
        except Exception as err:
            raise err
