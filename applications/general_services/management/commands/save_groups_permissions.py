import json
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404


class Command(BaseCommand):
    help = "create groups and permissions"

    def handle(self, *args, **kwargs):
        groups = Group.objects.all()
        data = {

        }
        permissions = []
        result = []
        for item in groups:
            print(permissions)
            data["group_name"] = item.name
            for x in item.permissions.all():
                permissions.append(x.name)
            data["permissions"] = permissions
            result.append(data)
            permissions = []
        file = f"{settings.BASE_DIR}/applications/general_services/management/commands/groups_and_permissions.json"
        with open(file, "w+") as open_file:
            json.dump(result, open_file)
