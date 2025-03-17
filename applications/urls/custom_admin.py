from django.urls import include, path

app_name = "admin_applications"
app_urls: dict = {
    "accounts": "applications.accounts.urls",
    "general_services": "applications.general_services.urls",
    "merchant": "applications.merchant.urls",
    "order": "applications.order.apis.custom_admin.urls",
    "product": "applications.product.apis.custom_admin.urls",
    # update me here
}

urlpatterns = []
for _url in app_urls:
    _path = path("", include(app_urls[_url], namespace=_url))
    urlpatterns.append(_path)
