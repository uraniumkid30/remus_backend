from datetime import datetime
from decimal import Decimal

from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from applications.wallet.models import Wallet, WalletHistory, TransactionRecord
from applications.merchant.models import RestaurantPlatformSettings
from .forms import WalletForm
from applications.merchant.models import Subscription
from applications.payment.integrations.services.factory import get_service


def get_admin_url(wallet):
    admin_wallet_url = f"admin:{wallet._meta.app_label}_"
    admin_wallet_url += f"{wallet._meta.model_name}_change"
    restaurant = wallet.restaurant
    platform = RestaurantPlatformSettings.objects.get(restaurant=restaurant,)
    path: str = reverse(
        admin_wallet_url,
        args=[wallet.id],
    )
    return f"{platform.api_domain}{path}"


def wallet_topup(request, id: str = None):
    form = WalletForm()
    if request.method == "POST":
        try:
            wallet = Wallet.objects.get(pk=id)
            sub = Subscription.objects.get(restaurant=wallet.restaurant)
        except Wallet.DoesNotExist:
            raise Http404("Wallet does not exist")
        except Subscription.DoesNotExist:
            raise Http404("Subscription does not exist")

        service = get_service(sub.payment_provider)
        amt = request.POST["amount"]
        data = service.send_money(
            wallet.restaurant.email,
            {
                "amount_paid": request.POST["amount"],
                "payment_method_meta": {
                    "number": request.POST["card_number"],
                    "cvv": int(request.POST["cvv"]),
                    "expiry_month": int(request.POST["expiry_month"]),
                    "expiry_year": int(request.POST["expiry_year"]),
                },
            },
        )
        if data:
            msg = f"Successfully credited wallet with {amt}"
            WalletHistory.objects.create(
                wallet=wallet,
                main_balance=wallet.amount + Decimal(amt),
                bonus_balance=wallet.bonus_balance,
                previous_balance=wallet.amount,
                new_balance=wallet.amount + Decimal(amt),
                description="wallet_topup",
                transaction_type="credit",
            )
            TransactionRecord.objects.create(
                reference=data.get("reference", ""),
                amount=amt,
                category="wallet_topup",
                transaction_date=datetime.now(),
                receiver="admin",
                sender=f"{wallet.restaurant.email}",
            )
            wallet.amount += Decimal(amt)
            wallet.save()

        else:
            msg = f"Fialed to credit wallet with {amt}. contact Admin"
        messages.add_message(request, messages.INFO, msg)
        return redirect(get_admin_url(wallet))

    return render(request, "topup_form.html", {"form": form})
