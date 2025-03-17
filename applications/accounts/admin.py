from typing import Iterable

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from conf.core.mixins.admin import ExportCsvMixin
from .models import User, UserProfile, Blacklist, Customer, DeviceInfo, PinVerification
from .forms import GroupAdminForm


class ExportUserCSVMixin(ExportCsvMixin):
    @classmethod
    def get_field_names(cls) -> list:
        return ["First Name", "Last Name", "Phone Number", "Email", "Created_at"]

    @classmethod
    def get_query_data(cls) -> list:
        return User.objects.all().values_list(
            "first_name", "last_name", "phone_no", "email", "created_at"
        )


class CustomUserAdmin(UserAdmin, ExportUserCSVMixin):
    list_display: Iterable = (
        "id",
        "first_name",
        "last_name",
        "username",
        "email",
        "phone_no",
        "created_at",
    )
    list_filter: Iterable = ("created_at", "is_active", "is_staff")
    search_fields: Iterable = ("phone_no", "email")
    ordering: Iterable = ("created_at",)
    fieldsets: Iterable = (
        (
            "Identity",
            {
                "fields": ("first_name", "last_name"),
            },
        ),
        (
            "Personal info",
            {
                "fields": (
                    "phone_no",
                    "email",
                    "username",
                    "password",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "role",
                )
            },
        ),
    )
    actions: Iterable = ["export_as_csv"]
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("role",)}),)


admin.site.unregister(Group)


class GroupAdmin(admin.ModelAdmin):
    # Use our custom form.
    form = GroupAdminForm
    # Filter permissions horizontal as well.
    filter_horizontal = ["permissions"]


class CustomerAdmin(admin.ModelAdmin):
    search_fields = ("email", "username")


class DeviceInfoAdmin(admin.ModelAdmin):
    search_fields = ("browser_id",)


admin.site.register(Group, GroupAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)
admin.site.register(Blacklist)
admin.site.register(PinVerification)
admin.site.register(DeviceInfo, DeviceInfoAdmin)
admin.site.register(Customer, CustomerAdmin)
