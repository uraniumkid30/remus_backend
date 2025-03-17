from .template import PermissionTemplate, PermissionStatement, PermissionEffect
from . enums import Actions, AvailableModels

chef_permission_items = [
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

chef_permissions = PermissionTemplate(
    Statement=chef_permission_items
)
