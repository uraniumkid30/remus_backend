from rest_framework import routers


from applications.merchant.apis.customers.views import (
    RestaurantViewSet,
    DeviceInfoViewSet,
)

router = routers.SimpleRouter()
router.register(r"restaurants", RestaurantViewSet, basename="restaurants")
router.register(r"device_info", DeviceInfoViewSet, basename="device_info")

app_name = "merchant_api"
urlpatterns = router.urls
