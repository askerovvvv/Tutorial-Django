from rest_framework.test import APITestCase

from django.urls import include, path, reverse
from course.models import Course, Category


class AdviserSerializerTestCase(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(slug='Programming')
        self.course = Course.objects.create(name='Programming', category=self.category)
        print(self.course)

    def test_get(self):
        url = reverse('lesson:dw')
        response = self.client.get(url, format='json')
        print(response)

