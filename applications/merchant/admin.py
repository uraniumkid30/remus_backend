from django.contrib import admin

from .models import (
    Company, MerchantProfile,
    MerchantPlatformSettings, QRScan,
    QRTag, Store, Subscription
)


admin.site.register(Company)
admin.site.register(MerchantProfile)
admin.site.register(MerchantPlatformSettings)
admin.site.register(QRTag)
admin.site.register(QRScan)
admin.site.register(Store)
admin.site.register(Subscription)
