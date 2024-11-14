import sys
import logging

import jwt
from jwt.exceptions import InvalidSignatureError
from django.conf import settings

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .responses.data import EmailViewResponses
from applications.general_services.managers.serializers import (
    EmailSerializer
)
from services.email_dispatcher import email_engine_factory


logger = logging.getLogger(__name__)


class EmailAPIView(APIView):
    """
    Sends an email
    """
    permission_classes = [AllowAny]
    serializer_class = EmailSerializer
    view_name = sys._getframe(0).f_code.co_name

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            sender = serializer.validated_data.get('sender')
            receipients = serializer.validated_data.get('receipients')
            body = serializer.validated_data.get('body')
            email_engine = email_engine_factory("SENTINEL")
            email_engine.send_mail(receipients, sender, body=body, subject="test")
            return Response(**EmailViewResponses.responses("email_sent"))

        return Response(**EmailViewResponses.responses())


