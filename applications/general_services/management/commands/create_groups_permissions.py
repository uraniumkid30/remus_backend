import json
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = "create groups and permissions"

    def handle(self, *args, **kwargs):
        file = f"{settings.BASE_DIR}/applications/general_services/management/commands/groups_and_permissions.json"
        with open(file, "r") as open_file:
            data = json.load(open_file)
        for item in data:
            group_name = item["group_name"]
            group, created = Group.objects.get_or_create(name=group_name)
            for perm in item["permissions"]:
                permission = Permission.objects.filter(name=perm)
                group.permissions.add(permission)
