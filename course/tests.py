import json
import tempfile
from io import StringIO
from io import BytesIO
import mock
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.fields.files import ImageFieldFile
from django.test import TestCase
from rest_framework import status
# from StringIO import StringIO
# in python 3: from io import StringIO
from PIL import Image
from django.core.files.base import File
from rest_framework.test import APITestCase, URLPatternsTestCase

from django.urls import include, path, reverse
from course.models import Course, Category
from course.serializers import CourseSerializer, CategorySerializer

import json

# class Object:
#     def toJSON(self):
#         return json.dumps(self, default=lambda o: o.__dict__,
#             sort_keys=True, indent=4)
#
# class ExtendedEncoder(DjangoJSONEncoder):
#     def default(self, o):
#         if isinstance(o, ImageFieldFile):
#             return str(o)
#         else:
#             return super().default(o)
#

class CourseTestApiCase(APITestCase, URLPatternsTestCase):
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

    @staticmethod
    def get_image_file(name='a.png', ext='png', size=(50, 50), color=(256, 0, 0)):
        file_obj = BytesIO()
        image = Image.new("RGBA", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    def test_post(self):
        url = reverse('course-list')
        data = {
            'id': 5,
            'name': 'Java',
            'category': 2,
            'likes': 0,
            'rating': 0,
            'comments': 0,
            'counter_lesson': []
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(data, response.data)

