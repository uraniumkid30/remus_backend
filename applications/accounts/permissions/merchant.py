from .template import PermissionTemplate, PermissionStatement, PermissionEffect
from . enums import Actions, AvailableModels

admin_permission_items = [
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

admin_permissions = PermissionTemplate(
    Statement=admin_permission_items
)
