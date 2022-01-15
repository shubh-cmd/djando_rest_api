import datetime
import email
from functools import partial
import random
import string

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import exceptions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .validators import CheckPermissions
from .models import User, PasswordReset
from .serializers import UserSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = get_object_or_404(User, email=email)

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password')

        token, created = Token.objects.get_or_create(user=user)

        return Response({"token": token.key, "email": token.user.email}, status=200)


class UserView(APIView):
    permission_classes = [IsAuthenticated | CheckPermissions]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self,request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)




class LogoutView(APIView):
    permission_classes = [IsAuthenticated | CheckPermissions]

    def post(self, request):
        try:
            Token.objects.get(user=request.user).delete()
        except Token.DoesNotExist:
            pass

        Token.objects.create(user=request.user)

        return Response(status=200)


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data['email']
        token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))

        PasswordReset.objects.create(email=email, token=token)

        send_mail(
            subject='reset your password',
            message='Click <a href="http://localhost:3000/reset/' + token + '"> here </a>to reset your password',
            from_email='admin@example.com',
            recipient_list=[email]
        )

        return Response({
            'message': 'please check your email!'
        })


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        if data['password'] != request.data['password_confirm']:
            raise exceptions.APIException('Password do not match')

        passwordReset = get_object_or_404(PasswordReset, token=data['token'])

        user = get_object_or_404(User, email=passwordReset.email)

        user.set_password(data['password'])
        user.save()

        return Response(status=200)
