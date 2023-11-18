import re
import sys
import logging

import jwt
from jwt.exceptions import InvalidSignatureError
from django.core.cache import cache
from conf.core.api.pagination import CustomPagination
from django.contrib.auth import authenticate, logout
from django.conf import settings

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from applications.accounts.models import User, UserProfile
from applications.accounts.managers.serializers import (
    LoginSerializer,
    DashboardSerializer,
    UserSerializer,
    RegistrationSerializer,
    ProfileUpdateSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
    ListUserSerializer
)


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
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            verification_token = serializer.validated_data.get('verification_token')
            if verification_token:
                try:
                    user_data = jwt.decode(verification_token, settings.SECRET_KEY, algorithms=['HS256'])
                    user_id = user_data['id']
                    user = User.objects.filter(id=user_id)
                except InvalidSignatureError:
                    user = None

                if user is None or not user.exists():
                    return Response(
                        {'message': "Invalid credentials", 'status': '00'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            user = authenticate(username=username, password=password)
            if user is None:
                return Response(
                    {'message': "Invalid password", 'status': '00'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            resp = {
                'status': '00',
                'token': user.token, 'id': user.id
            }
            return Response(resp, status=status.HTTP_200_OK)

        return Response({'message': "Invalid credentials", 'status': '00'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    """
    Logs in an existing user.
    """
    permission_classes = (IsAuthenticated,)
    view_name = sys._getframe(0).f_code.co_name

    def post(self, request, **args):
        if request.data.get('phone_no'):
            user = User.objects.get(phone_no=request.user.phone_no)
        user = User.objects.get(phone_no=request.user.phone_no)
        userprofile = UserProfile.objects.get(user=user)
        userprofile.available_online = False
        userprofile.save()
        logout(request)
        return Response(
            {
                'data':
                {"message": "Successfully logged out"}
            },
            status=status.HTTP_200_OK)


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            data = {
                'message': "Registration successful",
                "username": user.username,
                "email": user.email,
                "verification_token": user.token
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response({'message': "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class DashboardView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({
            'status': '00',
            'data': {}
        })


def session_update(session, **kwargs):
    if kwargs['field'] == 'auth':
        session['auth_tokens'][kwargs['token']] = kwargs
        session['auth_users'][kwargs['phone_no']] = kwargs
    else:
        session['reset_pw'][kwargs['email']] = kwargs
    return session


class ProfileUpdate(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileUpdateSerializer
    lookup_field = 'id'
    view_name = sys._getframe(0).f_code.co_name

    def get_object(self, id):
        try:
            user = User.objects.get(id=id)
            return UserProfile.objects.get(user=user), user
        except Exception as e:
            print(e)
            return None, None

    def put(self, request, id):
        if not id:
            msg = f"{self.ablogger.exx} user id supplied is not appropriate, i got {id}"
            logger_list = ['accounts', 'error']
            self.ablogger.save_transaction_info(msg, status=False, fn_name=self.view_name, loggernames=logger_list)
            data = {'message': 'network error please try again', 'status': '00'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            userprofile = self.get_object(id)[0]

        if not userprofile:
            msg = f"{self.ablogger.exx} This user has no user profile"
            logger_list = ['accounts', 'error']
            self.ablogger.save_transaction_info(msg, status=False, fn_name=self.view_name, loggernames=logger_list)
            return Response({'message': 'user does not exist', 'status': '00'}, status=status.HTTP_400_BAD_REQUEST)
        rdata = request.data
        serializer = self.serializer_class(userprofile, data=rdata)
        logger.info(rdata)
        logger.info(serializer.is_valid())
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'user profile updated', 'status': '00'}, status=status.HTTP_200_OK)
        return Response({'message': "Invalid credentials", 'status': '00'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = User.objects.get(phone_no=request.user.phone_no)
        data = {'first_name': user.first_name, 'last_name': user.last_name,
                'phone_no': user.phone_no, 'email': user.email,
                }

        if data['first_name'] or data['last_name']:
            message = "Profile is up to date"
        else:
            message = "Profile needs Update"
        return Response({'status': '00', 'user': data, 'message': message})


class ResetPasswordRequest(APIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetSerializer

    def get_object(self, phone_no):
        try:
            return User.objects.get(phone_no=phone_no)
        except:
            return None

    def post(self, request,):
        unregistered_email = request.data.get('email')
        request.data.pop('email', None)
        serializer = self.serializer_class(data=request.data)
        phone_no = request.data.get('phone_no')
        user = self.get_object(phone_no)
        
        if not user:
            data = {'message': 'This phone_no: {} , does not belong to any user on lottoly'.format(phone_no)}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        email = user.email
        if (not email) and (not unregistered_email):
            return Response({'message': 'This user does not have an email', 'status': '99'}, status=status.HTTP_200_OK)
        elif unregistered_email:
            user.email = unregistered_email
            user.save()
            email = unregistered_email
        if serializer.is_valid() and user:
            resp = {
                'status': '00',
                'email': email,
                'message': 'Please check your email to reset password'
            }
            return Response(resp, status=status.HTTP_200_OK)
        return Response({'message': 'wrong field query', }, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordConfirm(APIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetConfirmSerializer

    def get_object(self, email):
        try:
            return User.objects.get(email=email)
        except:
            return None

    def post(self, request,):
        serializer = self.serializer_class(data=request.data)
        password1 = request.data.get('password')
        password2 = request.data.get('confirm_password')
        email = request.data.get('email')
        user = self.get_object(email)
        logger.info(email)
        logger.info(user)
        logger.info('after user')
        if not user:
            return Response({'message':'This email: {} does not belong to any user on lottoly'.format(email),}, status=status.HTTP_400_BAD_REQUEST)
        pattern = services.PASSWORD_PATTERN
        if serializer.is_valid():
            if password1 != password2:
                return Response({'message': 'Password mismatch', 'status': '00'})
            if re.match(pattern, password1):
                user.set_password(password1)
                user.save()
                logger.info('user new password is {}'.format(password1))
                return Response({'message': 'Password ok, password reset', 'status': '00'})
            else:
                Response({'message': 'bad password'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'wrong field query'}, status=status.HTTP_400_BAD_REQUEST)


class UserListView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ListUserSerializer
    # filter_class = UserFilter
    queryset = User.objects.all()
    pagination_class = CustomPagination


class RetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer
    lookup_field = 'id'
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "User has been successfully deleted"},
                        status=status.HTTP_204_NO_CONTENT)


class PhoneLookUp(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request):
        ser_data = request.data
        ser_data['user'] = request.user.pk
        serializer = self.serializer_class(data=ser_data)
        phone_no = request.data.get('phone_no')
        resp, user = phonelookup(phone_no) 

        if resp != 'valid' and ((not user)):
            Response(phonelookup.phone_response[resp], status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.info(phonelookup.phone_response[resp])
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        response = {
            "message": "User is not registered with the system.",
            "status": "success"
        }
        return Response(response, status=status.HTTP_200_OK)
