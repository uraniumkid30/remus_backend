from .template import PermissionTemplate, PermissionStatement, PermissionEffect
from . enums import Actions, AvailableModels

waiter_permission_items = [
    PermissionStatement(
        **{
            "Effect": PermissionEffect.Allow,
            "Actions": [Actions.read, Actions.patch, Actions.list],
            "Resource": AvailableModels.orders
        }
    ),
    PermissionStatement(
        **{
            "Effect": PermissionEffect.Allow,
            "Actions": [Actions.read, Actions.patch, Actions.list],
            "Resource": AvailableModels.order_items
        }
    ),
    PermissionStatement(
        **{
            "Effect": PermissionEffect.Allow,
            "Actions": [Actions.read, Actions.patch, Actions.list],
            "Resource": AvailableModels.products
        }
    )
]

waiter_permissions = PermissionTemplate(
    Statement=waiter_permission_items
)
