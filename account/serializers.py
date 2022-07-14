from django.contrib.auth import get_user_model
from rest_framework import serializers

from account.send_mail import send_confirmation_email

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(min_length=6, write_only=True, required=True)
    class Meta:
        model = User
        fields = ('email', 'password', 'password2')

    def validate(self, attrs): # в 'attrs' прилетает то что мы отослали(email, password, password2) VALIDATE - проверка
        password = attrs.get('password') # данные 1 пароля
        password2 = attrs.pop('password2') # удаляем 2 пароль и сохраняем в переменной

        if password != password2:
            raise serializers.ValidationError('Password do not match')
        return attrs # Если все хорошо нужно возвращать все данные


    def create(self, validated_data): # логика регистрации
        user = User.objects.create_user(**validated_data) # принимает все данные которые прошли проверку
        code = user.activation_code  # наш активационный код передали новой переменной

        send_confirmation_email(code, user.email) # delay - указывает что он будет работать с celery
        return user