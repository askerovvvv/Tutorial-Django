from django.contrib.auth import get_user_model
from django.shortcuts import render
# from rest_framework.authtoken.views import ObtainAuthToken
#
#
# class LoginView(ObtainAuthToken):
#     serializer_class = LoginSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from account.serializers import RegisterSerializer, ForgotPasswordSerializer, ForgotPasswordCompleteSerializer, \
    UserProfileSerializer

User = get_user_model()


class RegisterApiView(APIView):
    """
    API for register User after it will send message to user email
    """
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            message = 'Вы успешно зарегистрированы. Вам отправлено письмо с активизацией'
            return Response(message, status=201)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ActivationView(APIView):
    """
    For activate user, it will in user's email like link
    """
    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response("ВЫ успешно активизировали свой аккаунт", status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response("Активационный код не действителен")


class ForgotPasswordApiView(APIView):
    """
    It will send activation code to user's email he must save it
    """
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_code()
            return Response('Вам отправлен активационыый код для смены пароля!')


class ForgotPasswordCompleteApiView(APIView):
    """
    user writes activation code that has sent before and after user can change password
    """
    def post(self, request):
        serializer = ForgotPasswordCompleteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.create_new_password()
            return Response('Пароль успешно обновлён')


class UserProfile(ListAPIView):
    """
    Usual User profile
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(email=self.request.user)
        return queryset

