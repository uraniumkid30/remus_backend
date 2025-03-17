from itertools import chain

from rest_framework import serializers
from django.db.models import F as Fquery, Q as Qquery
from django.contrib.auth.models import Group
from django.template.loader import render_to_string


from conf.core.serializers import EXCLUDED_TIME_FIELDS
from applications.order.models import Order, OrderItem
from applications.product.models import Product
from applications.accounts.api.serializers import (
    DeviceInfoSerializer,
    CustomerSerializer,
)
from applications.accounts.models import DeviceInfo, Customer
from services.email_dispatcher import email_engine_factory
from services.cloud.aws.utils import get_file_url


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        exclude = [*EXCLUDED_TIME_FIELDS]


class ReadOrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        exclude = [*EXCLUDED_TIME_FIELDS]


class OrderCheckoutSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    customer = CustomerSerializer()
    device = DeviceInfoSerializer()

    class Meta:
        model = Order
        fields = ["id", "order_items", "customer", "device", "table"]
        extra_kwargs = {
            "table": {"required": True},
            "id": {"read_only": True},
        }

    def create(self, validated_data):
        order_items = validated_data.pop("order_items")
        customer_data = validated_data.pop("customer")
        customer = self.get_or_create_customer(customer_data)
        device = DeviceInfo.objects.create(**validated_data.pop("device", {}))
        order = Order.objects.create(**validated_data)
        total = 0
        total_wait_time = 1
        for item in order_items:
            try:
                payload_quantity: int = item["quantity"]
                product = Product.objects.get(id=item["product"].id)
                _total = self.create_order_item(item, product, order, total_wait_time)
                total += _total
                self.update_product(product, payload_quantity)
            except Exception as err:
                print(err)
        order.total = total
        order.device = device
        order.customer = customer
        order.total_wait_time = total_wait_time
        order.save()
        return order

    def update_product(self, product, payload_quantity):
        if hasattr(product, "product_stocks"):
            new_quantity = Fquery("quantity") - payload_quantity
            product.product_stocks.quantity = new_quantity
        product.point += 1
        product.save()
        product.refresh_from_db()

    def create_order_item(self, item: dict, product, order, total_wait_time: int):
        item["price"] = product.final_price()
        item["product"] = product
        payload_quantity: int = item["quantity"]
        total = float(item["price"]) * payload_quantity
        if product.wait_time > total_wait_time:
            total_wait_time = product.wait_time
        OrderItem.objects.create(
            order=order,
            **item,
        )
        return total

    def get_or_create_customer(self, customer_data: dict):
        email = customer_data.get("email")
        customer_id = customer_data.get("customer_id")
        customer = None
        if email is not None:
            customer = Customer.objects.filter(Qquery(email=email))
        elif customer_id is not None:
            customer = Customer.objects.filter(Qquery(customer_id=customer_id))

        if customer and customer.exists():
            return customer.last()
        customer = Customer.objects.create(**customer_data)
        return customer

    def notify_employees(self, order):
        table_name = order.table.name
        order_number = order.order_number
        restaurant = order.table.restaurant
        url = order.first().get_admin_url()
        logo_url = get_file_url(restaurant.logo.name)
        body = render_to_string(
            "order_email.html",
            {
                "table_name": table_name,
                "order_url": url,
                "logo_url": logo_url,
            },
        )
        data = {
            "body": body,
            "subject": f"New Order {order_number}",
            "sender_name": "Order Menu",
            "to_name": "Waiters And Chefs",
        }
        to = self.get_receivers()
        _from = "new_order@donotreply.com"
        cl = email_engine_factory("sentinel")
        cl.send_mail(to, _from, **data)

    def get_receivers(self):
        result = []
        try:
            chef_group = Group.objects.get(name="chef")
            waiter_group = Group.objects.get(name="waiter")
            users = list(
                chain(
                    chef_group.user_set.all(),
                    waiter_group.user_set.all(),
                )
            )
            for _user in users:
                result.append(
                    {
                        "name": _user.get_full_name(),
                        "email": _user.email,
                    }
                )
        except Exception as err:
            print(err)
        finally:
            return result
