from rest_framework import serializers

from conf.core.serializers import EXCLUDED_TIME_FIELDS


from applications.order.models import Order, OrderItem


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
