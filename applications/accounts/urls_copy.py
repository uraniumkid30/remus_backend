from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from applications.accounts.api import (
    LoginAPIView,
    DashboardView,
    ResetPasswordRequest,
    ResetPasswordConfirm,
    ProfileUpdate,
    UserProfileView,
    UserRegistrationView,
    PhoneLookUp,
    LogoutAPIView,
)


router_v1 = DefaultRouter()
app_name: str = "users"
environment = settings.ENVIRONMENT
urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/register', UserRegistrationView.as_view(), name='user-registration'),
    path('auth/login', LoginAPIView.as_view(), name='user-login'),
    path('auth/user/dashboard', DashboardView.as_view(), name='dashboard'),
    path('auth/user/updateprofile/<str:id>', ProfileUpdate.as_view(), name='profileupdate'),
    path('auth/user/profile/', UserProfileView.as_view(), name='user-profile'),
    path('auth/logout', LogoutAPIView.as_view(), name='user-logout'),
    path('auth/phonelookup/', PhoneLookUp.as_view(), name='third-party-look-up'),
    path('auth/resetpassword/request', ResetPasswordRequest.as_view(), name='password-reset-request'),
    path('auth/resetpassword/confirm', ResetPasswordConfirm.as_view(), name='password-reset-confirm'),
]
