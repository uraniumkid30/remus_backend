import sys
import logging

from conf.core.api.pagination import CustomPageNumberPagination
from django.contrib.auth import authenticate, logout

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from applications.accounts.managers.selectors import (
    UserSelector,
)
from applications.accounts.api.serializers import (
    LoginSerializer,
    InitiateRegistrationSerializer,
    RegistrationSerializer,
    ListUserSerializer,
    UserSerializer,
    login_data
)
from applications.authentication.jwt import verify_new_user


logger = logging.getLogger(__name__)


class LoginAPIView(APIView):
    """
    Logs in an existing user.
    """

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    view_name = sys._getframe(0).f_code.co_name

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        print(request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data.get("username")
            password = serializer.validated_data.get("password")
            new_user = verify_new_user(serializer.validated_data)
            if new_user is None:
                return Response(
                    {"message": "Invalid credentials", "status": "00"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user = authenticate(username=username, password=password)
            if user is None:
                return Response(
                    {"message": "Invalid password", "status": "00"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            resp = login_data(UserSerializer(user).data, user)
            return Response(resp, status=status.HTTP_200_OK)

        return Response(
            {"message": "Invalid credentials", "status": "00"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserInitiateRegistrationView(APIView):
    permission_classes = [AllowAny]
    serializer_class = InitiateRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = {
                "message": "Registration successful pin sent",
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(
            {"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
        )


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if serializer.find_pin(request.data) is not None:
                user = serializer.save()
                data = {
                    "message": "Registration successful",
                    "username": user.username,
                    "email": user.email,
                    "verification_token": user.token,
                }
                return Response(data, status=status.HTTP_200_OK)
            return Response(
                {"message": "Invalid pin"}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {"message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST
        )


class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = UserSelector.fetch_record(phone_no=request.user.phone_no)
        data = UserSerializer(user).data
        return Response({"status": "00", "user": data})


class UserListView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ListUserSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return UserSelector.fetch_records()
