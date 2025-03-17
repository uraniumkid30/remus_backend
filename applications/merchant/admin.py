from datetime import datetime

from django.contrib import admin, messages

from .models import (
    MerchantProfile,
    RestaurantPlatformSettings,
    QRScan,
    QRTag,
    Restaurant,
    Subscription,
    Table,
    BankDetail,
    OperationSchedule,
    SubscriptionPricing,
    SubscriptionPayment,
    SocialAccount,
)
from applications.merchant.utils.subscriptions import (
    is_subscription_active,
)
from applications.wallet.models import (
    Wallet,
    WalletHistory,
    TransactionRecord,
)
from conf.core.utils import get_user_profile


class QRTagAdmin(admin.ModelAdmin):
    exclude = ("receipt",)
    readonly_fields = ("id", "qr_image", "domain", "created_at")

    def get_queryset(self, request):
        qs = super(QRTagAdmin, self).get_queryset(request)
        user_profile = get_user_profile(request)
        if user_profile and request.user.role == "admin":
            return qs
        elif user_profile and user_profile.restaurant:
            return qs.filter(table__restaurant__workers=user_profile)
        else:
            return qs.none()


class QRScanAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super(QRScanAdmin, self).get_queryset(request)
        user_profile = get_user_profile(request)
        if user_profile and request.user.role == "admin":
            return qs
        elif user_profile and user_profile.restaurant:
            return qs.filter(qr__table__restaurant__workers=user_profile)
        else:
            return qs.none()


class TableAdmin(admin.ModelAdmin):
    search_fields = ("name",)

    def get_queryset(self, request):
        qs = super(TableAdmin, self).get_queryset(request)
        user_profile = get_user_profile(request)
        if user_profile and request.user.role == "admin":
            return qs
        elif user_profile and user_profile.restaurant:
            return qs.filter(restaurant__workers=user_profile)
        else:
            return qs.none()


class SubscriptionAdmin(admin.ModelAdmin):
    search_fields = ("restaurant",)
    list_display = [
        "restaurant",
        "category",
        "billing_cycle",
        "status",
        "is_active",
    ]
    list_filter = [
        "status",
        "category",
        "billing_cycle",
        "subscription_price",
    ]

    def is_active(self, obj):
        return is_subscription_active({"id": obj.id})

    is_active.short_description = "Is Service Active"
    is_active.boolean = True

    def get_queryset(self, request):
        qs = super(SubscriptionAdmin, self).get_queryset(request)
        user_profile = get_user_profile(request)
        if user_profile and request.user.role == "admin":
            return qs
        elif user_profile and user_profile.restaurant:
            return qs.filter(restaurant__workers=user_profile)
        else:
            return qs.none()


class SubscriptionPaymentAdmin(admin.ModelAdmin):
    change_form_template = "pay_subscription.html"

    def response_change(self, request, obj):
        if "_pay-subscription" in request.POST:
            restaurant = obj.subscription.restaurant
            wallet = Wallet.objects.get(restaurant=restaurant)
            if wallet.amount > obj.subscription.total_price:
                amt = obj.subscription.total_price
                WalletHistory.objects.create(
                    wallet=wallet,
                    main_balance=wallet.amount - amt,
                    bonus_balance=wallet.bonus_balance,
                    previous_balance=wallet.amount,
                    new_balance=wallet.amount - amt,
                    description="subscription",
                    transaction_type="debit",
                )
                TransactionRecord.objects.create(
                    reference=str(obj.subscription.id),
                    amount=amt,
                    category="subscription",
                    transaction_date=datetime.now(),
                    receiver=f"restaurant {wallet.restaurant}",
                    sender=f"{wallet.restaurant.email}",
                )
                wallet.amount -= obj.subscription.total_price
                wallet.save()
                obj.amount = obj.subscription.total_price
                obj.status = "paid"
                obj.payment_date = datetime.now()
                obj.save()
            else:
                msg = "Insufficient funds in wallet"
                messages.add_message(request, messages.INFO, msg)
        return super().response_change(request, obj)

    search_fields = ("subscription",)
    list_display = [
        "subscription",
        "status",
        "amount",
    ]
    list_filter = [
        "status",
    ]

    def get_queryset(self, request):
        qs = super(SubscriptionPaymentAdmin, self).get_queryset(request)
        user_profile = get_user_profile(request)
        if user_profile and request.user.role == "admin":
            return qs
        elif user_profile and user_profile.restaurant:
            return qs.filter(subscription__restaurant__workers=user_profile)
        else:
            return qs.none()


class RestaurantAdmin(admin.ModelAdmin):
    search_fields = ("name", "slug")
    list_display = [
        "name",
        "slug",
        "email",
    ]
    fieldsets = [
        (
            "Identification",
            {
                "fields": [
                    "restaurant_id",
                    "merchant",
                    "name",
                    # "slug",
                    "short_note",
                ],
            },
        ),
        (
            "Contact",
            {
                "classes": ["wide"],
                "fields": ["email", "telephone"],
            },
        ),
        (
            "Images",
            {
                "classes": ["wide"],
                "fields": [
                    "logo",
                    "logo_inside_qr_code",
                    "background",
                    "receipt_thumbnail",
                ],
            },
        ),
    ]

    def get_queryset(self, request):
        qs = super(RestaurantAdmin, self).get_queryset(request)
        user_profile = get_user_profile(request)
        if user_profile and request.user.role == "admin":
            return qs
        elif user_profile and user_profile.restaurant:
            return qs.filter(workers=user_profile)
        else:
            return qs.none()


class BankDetailAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super(BankDetailAdmin, self).get_queryset(request)
        user_profile = get_user_profile(request)
        if user_profile and request.user.role == "admin":
            return qs
        elif user_profile and user_profile.restaurant:
            return qs.filter(restaurant__workers=user_profile)
        else:
            return qs.none()


class SocialAccountAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super(SocialAccountAdmin, self).get_queryset(request)
        user_profile = get_user_profile(request)
        if user_profile and request.user.role == "admin":
            return qs
        elif user_profile and user_profile.restaurant:
            return qs.filter(restaurant__workers=user_profile)
        else:
            return qs.none()


class OperationScheduleAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super(OperationScheduleAdmin, self).get_queryset(request)
        user_profile = get_user_profile(request)
        if user_profile and request.user.role == "admin":
            return qs
        elif user_profile and user_profile.restaurant:
            return qs.filter(restaurant__workers=user_profile)
        else:
            return qs.none()


class MerchantProfileAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(MerchantProfileAdmin, self).get_queryset(request)
        user_profile = get_user_profile(request)
        if user_profile and request.user.role == "admin":
            return qs
        elif user_profile and user_profile.restaurant:
            return qs.filter(user__userprofile=user_profile)
        else:
            return qs.none()


class RestaurantPlatformSettingsAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super(RestaurantPlatformSettingsAdmin, self).get_queryset(request)
        user_profile = get_user_profile(request)
        if user_profile and request.user.role == "admin":
            return qs
        elif user_profile and user_profile.restaurant:
            return qs.filter(restaurant__workers=user_profile)
        else:
            return qs.none()


admin.site.register(QRTag, QRTagAdmin)
admin.site.register(QRScan, QRScanAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(SubscriptionPayment, SubscriptionPaymentAdmin)
admin.site.register(Table, TableAdmin)
admin.site.register(SubscriptionPricing)
admin.site.register(BankDetail, BankDetailAdmin)
admin.site.register(SocialAccount, SocialAccountAdmin)
admin.site.register(OperationSchedule, OperationScheduleAdmin)
admin.site.register(MerchantProfile, MerchantProfileAdmin)
admin.site.register(RestaurantPlatformSettings, RestaurantPlatformSettingsAdmin)
