from django.urls import include, path

app_name = "applications"
app_urls: dict = {
    "accounts": "applications.accounts.urls",
    "general_services": "applications.general_services.urls",
    #update me here
}

urlpatterns = [ path("", include(app_urls[_url])) for _url in app_urls]
