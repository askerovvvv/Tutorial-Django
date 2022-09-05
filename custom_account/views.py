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


from custom_account.serializers import RegisterSerializer, ForgotPasswordSerializer, ForgotPasswordCompleteSerializer, \
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
            message = 'You have successfully registered. An activation email has been sent to you.'
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
            return Response("YOU have successfully activated your account", status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response("Activation code is not valid")


class ForgotPasswordApiView(APIView):
    """
    It will send activation code to user's email he must save it
    """
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_code()
            return Response('An activation code has been sent to you to change your password.!')


class ForgotPasswordCompleteApiView(APIView):
    """
    user writes activation code that has sent before and after user can change password
    """
    def post(self, request):
        serializer = ForgotPasswordCompleteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.create_new_password()
            return Response('Password updated successfully')


class UserProfile(ListAPIView):
    """
    Usual User profile
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

