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

from account.serializers import RegisterSerializer, ForgotPasswordSerializer, ForgotPasswordCompleteSerializer

User = get_user_model()


class RegisterApiView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            message = 'Вы успешно зарегистрированы. Вам отправлено письмо с активизацией'
            return Response(message, status=201)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ActivationView(APIView):
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
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_code()
            return Response('Вам отправлен активационыый код для смены пароля!')


class ForgotPasswordCompleteApiView(APIView):
    def post(self, request):
        serializer = ForgotPasswordCompleteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.create_new_password()
            return Response('Пароль успешно обновлён')


