from django.contrib import admin

from .models import (
    Company, MerchantProfile,
    MerchantPlatformSettings, QRScan,
    QRTag, Store, Subscription, PointOfSale
)

class QRTagAdmin(admin.ModelAdmin):
    exclude = ('receipt', )
    readonly_fields = ('id', 'qr_image', 'domain', 'created_at')

admin.site.register(Company)
admin.site.register(MerchantProfile)
admin.site.register(MerchantPlatformSettings)
admin.site.register(QRTag, QRTagAdmin)
admin.site.register(QRScan)
admin.site.register(Store)
admin.site.register(Subscription)
admin.site.register(PointOfSale)
