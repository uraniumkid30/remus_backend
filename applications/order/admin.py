from django.contrib import admin
from . import models
from .forms import OrderAdminForm, SubOrderAdminForm
from conf.core.utils import get_user_profile


class OrderItemsInline(admin.TabularInline):
    model = models.OrderItem
    fields = ["product", "quantity", "price", "discount"]
    readonly_fields = ("product",)
    extra = 0
    show_change_link = True
    show_url = True


class OrderAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    list_display = [
        "order_number",
        "table",
        "total",
        "total_wait_time",
        "order_items_count",
        "status",
        "payment_status",
        "created_at",
    ]
    readonly_fields = [
        "order_number",
        "total",
        "total_wait_time",
    ]
    list_filter = (
        "status",
        "payment_status",
    )
    inlines = [
        OrderItemsInline,
    ]
    search_fields = [
        "id",
        "order_number",
    ]
    autocomplete_fields = [
        "table",
        "device",
    ]

    def get_form(self, request, obj=None, **kwargs):
        if request.user.role == "admin":
            kwargs["form"] = OrderAdminForm
        else:
            kwargs["form"] = SubOrderAdminForm
        return super().get_form(request, obj, **kwargs)

    def get_actions(self, request):
        actions = super(OrderAdmin, self).get_actions(request)
        if request.user.role != "admin":
            try:
                del actions["delete_selected"]
            except KeyError:
                pass
        return actions

    def has_delete_permission(self, request, obj=None):
        if request.user.role != "admin":
            return False
        return True

    def order_items_count(self, obj):
        return obj.order_items.count()

    def get_queryset(self, request):
        qs = super(OrderAdmin, self).get_queryset(request)
        user_profile = get_user_profile(request)
        if user_profile and request.user.role == "admin":
            return qs
        elif user_profile and user_profile.restaurant:
            return qs.filter(table__restaurant__workers=user_profile)
        else:
            return qs.none()


class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "product__name",
        "order__order_number",
        "quantity",
        "price",
        "created_at",
    ]
    search_fields = ["order__order_number", "order__id"]
    autocomplete_fields = ["order"]

    def get_queryset(self, request):
        qs = super(OrderItemAdmin, self).get_queryset(request)
        user_profile = get_user_profile(request)
        if user_profile and request.user.role == "admin":
            return qs
        elif user_profile and user_profile.restaurant:
            return qs.filter(order__table__restaurant__workers=user_profile)
        else:
            return qs.none()


class TableAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "table",
        "device",
        "expires_at",
    ]
    search_fields = ["table__name"]
    autocomplete_fields = ["table"]

    def get_queryset(self, request):
        qs = super(TableAdmin, self).get_queryset(request)
        user_profile = get_user_profile(request)
        if user_profile and request.user.role == "admin":
            return qs
        elif user_profile and user_profile.restaurant:
            return qs.filter(restaurant__workers=user_profile)
        else:
            return qs.none()


admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem, OrderItemAdmin)
admin.site.register(models.TableSession, TableAdmin)
