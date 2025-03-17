from django.urls import path

from . import views


app_name = 'merchant'

urlpatterns = [
    path(
        'qr/<uuid:qrtag_id>/',
        views.request_menu,
        name='qr_request_menu'
    )

]
