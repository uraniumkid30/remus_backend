from rest_framework import routers


from applications.order.apis.custom_admin.views import OrderViewSet
router = routers.SimpleRouter()
router.register(r'orders', OrderViewSet, basename='orders')

app_name = 'order'
urlpatterns = router.urls
