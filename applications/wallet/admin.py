from django.contrib import admin
from conf.core.mixins.admin import ExportCsvMixin
from django.urls import reverse
from django.shortcuts import redirect

from .models import Wallet, WalletHistory, TransactionRecord
from .forms import WalletAdminForm, SubWalletAdminForm
from conf.core.utils import get_user_profile


class WalletAdmin(admin.ModelAdmin, ExportCsvMixin):
    ...
    change_form_template = "wallet_topup.html"

    def response_change(self, request, obj):
        if "_wallet-topup" in request.POST:
            rev = reverse("wallet:wallet_topup", kwargs={"id": obj.id})
            return redirect(rev)
        return super().response_change(request, obj)

    def get_queryset(self, request):
        qs = super(WalletAdmin, self).get_queryset(request)
        user_profile = get_user_profile(request)
        if user_profile and request.user.role == "admin":
            return qs
        elif user_profile and user_profile.restaurant:
            return qs.filter(restaurant__workers=user_profile)
        else:
            return qs.none()

    def get_form(self, request, obj=None, **kwargs):
        if request.user.role == "admin":
            kwargs["form"] = WalletAdminForm
        else:
            kwargs["form"] = SubWalletAdminForm
        return super().get_form(request, obj, **kwargs)


class WalletHistoryAdmin(admin.ModelAdmin, ExportCsvMixin):

    def get_queryset(self, request):
        qs = super(WalletHistoryAdmin, self).get_queryset(request)
        user_profile = get_user_profile(request)
        if user_profile and request.user.role == "admin":
            return qs
        elif user_profile and user_profile.restaurant:
            return qs.filter(wallet__restaurant__workers=user_profile)
        else:
            return qs.none()


admin.site.register(Wallet, WalletAdmin)
admin.site.register(WalletHistory, WalletHistoryAdmin)
admin.site.register(TransactionRecord)
