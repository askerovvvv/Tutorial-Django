from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import serializers

from account.send_mail import send_confirmation_email

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    Usual RegisterSerializer
    """

    password2 = serializers.CharField(min_length=6, write_only=True, required=True)
    class Meta:
        model = User
        fields = ('email', 'password', 'password2')

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.pop('password2')

        if password != password2:
            raise serializers.ValidationError('Password do not match')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        code = user.activation_code
        send_confirmation_email(code, user.email)
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    """
    Serializer checks email if email in database it will send activation code to change password
    """
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Аккаунт не найден!')
        return email

    def send_code(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        user.save()
        send_mail(
            'Восстановление пароля Tutorial_v2',
            f'Код подтверждение:{user.activation_code}',
            'bekbol.2019@gmail.com',
            [email]
        )


class ForgotPasswordCompleteSerializer(serializers.Serializer):
    """
    Serializer checks email if email in database it will check password1 and password2 if it is True Serializer change
    password
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True, min_length=6)
    activation_code = serializers.CharField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Аккаунт не найден!')
        return email

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        code = attrs.get('activation_code')
        email = attrs.get('email')

        if password != password2:
            raise serializers.ValidationError('Пароли не совпадают!')

        if not User.objects.filter(activation_code=code, email=email).exists():
            raise serializers.ValidationError('Неверный активационный код!')
        return attrs

    def create_new_password(self):
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        user = User.objects.get(email=email)
        user.set_password(password)
        user.activation_code = ''
        user.save()


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Usual Serializer for user Serializer it shows now all fields
    """
    class Meta:
        model = User
        fields = ('date_joined', 'email', 'is_active', 'is_superuser')

