from django.urls import include, path

app_name = "customer_applications"
app_urls: dict = {
    "merchant": "applications.merchant.urls",
    "merchant_api": "applications.merchant.apis.customers.urls",
    "product": "applications.product.apis.customers.urls",
    "order": "applications.order.apis.customers.urls",
    "report": "applications.reports.apis.customers.urls",
    "payment": "applications.payment.apis.customers.urls",
    # update me here
}

urlpatterns = []
for _url in app_urls:
    _path = path("", include(app_urls[_url], namespace=_url))
    urlpatterns.append(_path)
