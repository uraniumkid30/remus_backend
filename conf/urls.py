from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from admin_notification.views import check_notification_view

admin.site.site_header = "Custom Administration"

admin.autodiscover()
customer_app = "applications.urls.customers"
customer_app_name = "customer_apis"
custom_admin_app = "applications.urls.custom_admin"
custom_admin_app_name = "custom_admin_apis"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("admin_tools_stats/", include("admin_tools_stats.urls")),
    path(
        "",
        include("applications.wallet.urls", namespace="wallet"),
    ),
    path(
        f"api/{settings.API_VERSION}/customers/",
        include(customer_app, namespace=customer_app_name),
    ),
    path(
        f"api/{settings.API_VERSION}/custom_admin/",
        include(custom_admin_app, namespace=custom_admin_app_name),
    ),
    path(
        f"api/{settings.API_VERSION}/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    # # Optional UI:
    path(
        f"api/{settings.API_VERSION}/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        f"api/{settings.API_VERSION}/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path(
        "check/notification",
        check_notification_view,
        name="check_notifications"
    ),
]


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
