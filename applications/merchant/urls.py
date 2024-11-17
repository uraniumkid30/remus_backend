from django.urls import path

from . import views


app_name = 'merchant'

urlpatterns = [
    path(
        'qr/<uuid:qrtag_id>/',
        views.request_receipt,
        name='qr_request_receipt'
    ),
    path(
        'custom_route/',
        views.custom_route,
        name='custom_route'
    ),

]
