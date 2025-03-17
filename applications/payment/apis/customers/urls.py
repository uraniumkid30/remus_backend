from rest_framework import routers


from applications.payment.apis.customers.views import PaymentViewSet
router = routers.SimpleRouter()
router.register(r'payments', PaymentViewSet, basename='payments')

app_name = 'payment'
urlpatterns = router.urls
