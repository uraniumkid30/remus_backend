from rest_framework import routers


from applications.product.apis.customers.views import (
    ProductViewSet,
    CategoryViewSet,
    RestaurantCategoryViewSet,
)

router = routers.SimpleRouter()
router.register(r"products", ProductViewSet, basename="products")
router.register(
    r"categories",
    CategoryViewSet,
    basename="categories",
)
router.register(
    r"restaurant/(?P<restaurant_id>[^/.]*)/categories",
    RestaurantCategoryViewSet,
    basename="restaurant_categories",
)
# r"restaurant/(?P<restaurant_id>[^/.]*)/categories",

app_name = "product"
urlpatterns = router.urls
