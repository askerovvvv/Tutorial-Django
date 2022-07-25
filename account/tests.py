from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

User = get_user_model()


class AccountTestCase(TestCase):
    def setUp(self):
        self.user = {
            'email': 'test@gmail.com',
            'password': '123456',
            'password2': '123456',
            'is_active': True
        }

    def test_register(self):
        url = reverse('register')
        response = self.client.post(url, self.user)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual('Вы успешно зарегистрированы. Вам отправлено письмо с активизацией', response.data)
        self.assertTrue(1, User.objects.all().count())

    def test_invalid_register(self):
        invalid_user = {
            'email': 'test@gmail.com',
            'password': '654321',
            'password2': '123456'
        }
        url = reverse('register')
        response = self.client.post(url, invalid_user)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(0, User.objects.all().count())
