from rest_framework import serializers
from django.db.models import F as Fquery

from conf.core.serializers import EXCLUDED_TIME_FIELDS
from applications.order.models import Order, OrderItem
from applications.product.models import Product


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        exclude = [*EXCLUDED_TIME_FIELDS]


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        exclude = [*EXCLUDED_TIME_FIELDS]
        extra_kwargs = {
            "table": {"required": True},
        }

    def create(self, validated_data):
        order_items = validated_data.pop("order_items")
        order = Order.objects.create(**validated_data)
        total = 0
        total_wait_time = 1
        for item in order_items:
            try:
                product = Product.objects.get(id=item["product"].id)
                item["price"] = product.final_price()
                item["product"] = product
                payload_quantity: int = item["quantity"]
                total += float(item["price"]) * payload_quantity
                if product.wait_time > total_wait_time:
                    total_wait_time = product.wait_time
                OrderItem.objects.create(
                    order=order,
                    **item,
                )
                if product.product_stocks:
                    new_quantity = Fquery("quantity") - payload_quantity
                    product.product_stocks.quantity = new_quantity
                    product.save()
                    product.refresh_from_db()
            except Exception as err:
                print(err)
        order.total = total
        order.total_wait_time = total_wait_time
        order.save()
        return order
