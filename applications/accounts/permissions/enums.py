from dataclasses import dataclass


@dataclass(frozen=True)
class AvailableModels:
    orders: str = "orders"
    order_items: str = "order_items"
    products: str = "products"
    categories: str = "categories"
    sub_categories: str = "sub_categories"
    coupons: str = "coupons"
    discounts: str = "discounts"
    users: str = "users"
    records: str = "records"


@dataclass(frozen=True)
class Actions:
    read: str = "read"
    list: str = "list"
    write: str = "write"
    full_edit: str = "full_edit"
    patch: str = "patch"
    delete: str = "delete"


@dataclass(frozen=True)
class ActionToMethod:
    read: str = "get"
    list: str = "get"
    write: str = "post"
    full_edit: str = "put"
    patch: str = "patch"
    delete: str = "delete"
