from rest_framework import routers


from applications.reports.apis.customers.views import ReportViewSet
router = routers.SimpleRouter()
router.register(r'reports', ReportViewSet, basename='reports')

app_name = 'report'
urlpatterns = router.urls
