from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import UpdateAPIView

from django.core.files.base import ContentFile
from django.utils.translation import gettext_lazy as _
from users import models
from users.api import serializers


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request, *args, **kwargs):
        name = request.data['nombres']
        last_name = request.data['apellidos']
        password = request.data['password']
        email = request.data['email']

        if models.User.objects.filter(email=email).exists():
            return Response({'error': 'Ya existe un usuario con este email'}, status=status.HTTP_400_BAD_REQUEST)

        user = models.User.objects.create_user(first_name=name,
                                               last_name=last_name,
                                               password=password,
                                               username=email,
                                               email=email)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request, *args, **kwargs):
        email = request.data['email']
        password = request.data['password']
        user = models.User.objects.filter(email=email).first()
        if user and user.check_password(password):
            token, _ = Token.objects.get_or_create(user=user)
            return Response(serializers.UserSerializer(user).data, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)