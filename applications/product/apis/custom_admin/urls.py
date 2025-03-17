from rest_framework import routers


from applications.product.apis.custom_admin.views import ProductViewSet, CategoryViewSet

router = routers.SimpleRouter()
router.register(r"products", ProductViewSet, basename="products")
router.register(r"categories", CategoryViewSet, basename="categories")

app_name = "product"
urlpatterns = router.urls
