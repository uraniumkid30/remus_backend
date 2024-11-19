from applications.merchant.models import MerchantPlatformSettings


def merchant_domain(store):
    try:
        merchant = store.merchant
        try:
            platform_site = merchant.platform_settings
            return platform_site.domain
        except MerchantPlatformSettings.DoesNotExist:
            pass
        platform_site = merchant.platform_settings
        domain = platform_site.domain
        return domain
    except (MerchantPlatformSettings.DoesNotExist, Exception):
        return ""


def get_merchant_domain(merchant):
    try:
        platform_site = merchant.platform_settings
        domain = platform_site.domain
        return domain
    except (MerchantPlatformSettings.DoesNotExist, Exception):
        return ""

