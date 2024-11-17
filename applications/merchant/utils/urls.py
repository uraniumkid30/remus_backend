from django.contrib.sites.models import Site

from merchant.models import MerchantPlatformSettings


def merchant_domain(store):
    try:
        merchant = store.merchant
        try:
            platform_site = merchant.platform_settings
            return platform_site.site.domain
        except MerchantPlatformSettings.DoesNotExist:
            pass
        platform_site = merchant.platform_settings
        domain = platform_site.site.domain
        return domain
    except (MerchantPlatformSettings.DoesNotExist, Exception):
        return Site.objects.get_current().domain


def get_merchant_domain(merchant):
    try:
        platform_site = merchant.platform_settings
        domain = platform_site.site.domain
        return domain
    except (MerchantPlatformSettings.DoesNotExist, Exception):
        return Site.objects.get_current().domain


def get_merchant_website_from_platform_request():
    default_url = ''
    current_site = Site.objects.get_current()
    merchant_platform = current_site.merchant_platform.first()
    if merchant_platform:
        merchant_website = merchant_platform.merchant.website
        return merchant_website
    return default_url
