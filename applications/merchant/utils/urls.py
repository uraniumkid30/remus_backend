from applications.merchant.models import (
    RestaurantPlatformSettings,
    MerchantProfile,
    Restaurant,
)

def get_restaurant_api_domain(restaurant):
    try:
        try:
            platform_site = restaurant.platform_setting
            return platform_site.api_domain
        except RestaurantPlatformSettings.DoesNotExist:
            pass
        except Exception as er:
            print(er)
        return ""
    except (Restaurant.DoesNotExist, Exception) as err:
        print(err)
        return ""
