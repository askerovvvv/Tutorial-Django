import json
import tempfile
import io

from io import StringIO

import mock
from django.conf import settings
from django.conf.urls.static import static
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

class CourseTestApiCase(APITestCase):
    # urlpatterns = [
    #     path('api/', include('course.urls')),
    # ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    def setUp(self):
        self.category = Category.objects.create(slug='Programming')
        self.course1 = Course.objects.create(name='Python', category=self.category, )
        self.course2 = Course.objects.create(name='JS', category=self.category, )
        self.category1 = CategorySerializer(self.category).data

        self.serializer_data = CourseSerializer([self.course1, self.course2], many=True).data

        # example_photo = Image.new(mode='RGB', size=(30, 60))
        # example_photo.save('testing.jpg')
        # with open('testing.jpg', 'rb') as img:
        #     self.photo = SimpleUploadedFile('testing.png',
        #                                     img.read(),
        #                                     content_type='image/png')
        image = io.BytesIO()
        Image.new('RGB', (150, 150)).save(image, 'JPEG')
        image.seek(0)
        self.file = SimpleUploadedFile('image.jpg', image.getvalue())

    def test_get(self):
        url = reverse('course-list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.serializer_data, response.data)
        self.assertEqual(len(self.serializer_data), len(response.data))

    def test_post(self):
        self.data = {
            'id': 3,
            'name': 'Java',
            'course_image': self.file,
            'category': 1,
            'likes': 0,
            'rating': 0,
            'comments': 0,
            'counter_lesson': [],
        }
        url = reverse('course-list')
        response = self.client.post(url, self.data, format='multipart')
        print(response.json())
        print('-----------------')
        print(self.data)
        print(response.data)
        self.assertEqual(self.data, response.data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

