from django.urls import path

from . import views

app_name = 'wallet'
urlpatterns = [
    path("wallet/<uuid:id>/topup/", views.wallet_topup, name="wallet_topup"),
]