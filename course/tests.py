from django.test import TestCase

from rest_framework.test import APITestCase, URLPatternsTestCase

from django.urls import include, path, reverse
from course.models import Course, Category


class AdviserSerializerTestCase(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/', include('course.urls')),
    ]

    def setUp(self):
        self.category = Category.objects.create(slug='Programming')
        self.course = Course.objects.create(name='Programming', category=self.category)
        print(self.course)

    def test_get(self):
        url = reverse('course-list')
        response = self.client.get(url)
        print(response.status_code)
