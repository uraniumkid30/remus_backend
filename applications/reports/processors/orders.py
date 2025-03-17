from django.db.models import Sum, Avg, Min, Max, Count

from applications.order.models import Order, OrderItem
from applications.product.models import Product
from applications.merchant.models import Table

# product with highest rating
# most ordered product
# total orders (product sold)
# total products
# total scans
# total sales amount
# table with the highest order
# time and day we have the highest order
# least ordered product
# last 10 orders sold
# current pending orders
total_orders_sold = Order.objects.aggregate(total_orders_sold=Count("id"))
total_orders = Order.objects.aggregate(total_orders=Count("id"))