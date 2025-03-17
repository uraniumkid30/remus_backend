import uuid

from rest_framework.exceptions import ValidationError

from applications.order.models import TableSession


def custom_query_params_check(query_params: dict):
    data = {}
    for item in query_params:
        if "session" == item:
            session_id = uuid.UUID(query_params[item])
            session = TableSession.objects.get(id=session_id)
            if session.is_expired():
                raise ValidationError("Session is expired")
            data["table"] = session.table.id
        else:
            data[item] = query_params[item]
    return data


def get_order_items_summary(order):
    items = []
    total = 0
    discount = 0
    for item in order.order_items.all():
        items.append(
            {
                "name": item.product.name,
                "quantity": int(item.quantity),
                "unit_price": item.price,
                "amount": float(item.price * item.quantity),
            }
        )
        discount += item.discount
        total += item.price * item.quantity
    return {
        "items": items,
        "total": float(total),
        "discount": float(discount),
    }
