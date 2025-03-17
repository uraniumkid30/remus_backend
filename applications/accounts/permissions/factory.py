from .chef import chef_permissions
from .waiter import waiter_permissions
from .merchant import admin_permissions


def get_role_permissions(role: str):
    if role == "chef":
        return chef_permissions.to_dict()
    elif role == "waiter":
        return waiter_permissions.to_dict()
    elif role == "merchant":
        return admin_permissions.to_dict()
