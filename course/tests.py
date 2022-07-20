import json
from django.test import TestCase
from rest_framework import status

from rest_framework.test import APITestCase, URLPatternsTestCase

from django.urls import include, path, reverse
from course.models import Course, Category
from course.serializers import CourseSerializer, CategorySerializer


class AdviserSerializerTestCase(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/', include('course.urls')),
    ]

    def setUp(self):
        self.category = Category.objects.create(slug='Programming')
        self.course1 = Course.objects.create(name='Python', category=self.category)
        self.course2 = Course.objects.create(name='JS', category=self.category)
        self.category1 = CategorySerializer(self.category).data
        self.serializer_data = CourseSerializer([self.course1, self.course2], many=True).data

    def test_get(self):
        url = reverse('course-list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.serializer_data, response.data)
        self.assertEqual(len(self.serializer_data), len(response.data))

    def test_post(self):
        a = Course.objects.create(name='mgew', course_image='a.jpg', category=self.category)
        b=a.course_image
        url = reverse('course-list')
        response = self.client.get(url)
        data = {
            'name': 'Java',
            'course_image': b,
            'category': 1
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        print(response.json())

