from django.conf import settings
from django.urls import path, include

from applications.general_services.api import (
    EmailAPIView
)


app_name: str = "general_services"
environment: str = settings.ENVIRONMENT
urlpatterns = [
    path('services/send_email', EmailAPIView.as_view(), name='send-email'),
]
