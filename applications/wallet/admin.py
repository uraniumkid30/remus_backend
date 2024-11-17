from django.contrib import admin

from .models import (
    Wallet,
    WalletHistory,
    TransactionRecord,
    MoneyRequest
)


admin.site.register(Wallet)
admin.site.register(WalletHistory)
admin.site.register(TransactionRecord)
admin.site.register(MoneyRequest)
