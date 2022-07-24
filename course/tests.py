import json
import tempfile
import io

from io import StringIO

import mock
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import get_user_model
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
User = get_user_model()

class CourseTestApiCase(APITestCase):
    # urlpatterns = [
    #     path('api/', include('course.urls')),
    # ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    def setUp(self):
        self.category = Category.objects.create(slug='Programming')
        self.course1 = Course.objects.create(name='Python', category=self.category, )
        self.course2 = Course.objects.create(name='JS', category=self.category, )
        self.category1 = CategorySerializer(self.category).data
        self.user = User.objects.create(email='testuser@gmail.com', is_staff=True)
        self.serializer_data = CourseSerializer([self.course1, self.course2], many=True).data
        self.client.force_authenticate(user=self.user)
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
        url = reverse('course-list')
        self.data = {
            'id': 3,
            'name': 'Java',
            'course_image': self.file,
            'category': self.category.id,
            'likes': 0,
            'rating': 0,
            'comments': 0,
            'counter_lesson': [],
        }
        response = self.client.post(url, self.data, format='multipart')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # self.assertTrue(f'media/courseimage/image_mryWGaN.jpg' in response.data['course_image'])
        self.assertEqual(3, Course.objects.all().count())

    def test_update(self):
        url = reverse('course-detail', args=(self.course1.id,))
        self.data = {
            'id': 3,
            'name': 'test name',
            'course_image': self.file,
            'category': self.category.id,
            'likes': 0,
            'rating': 0,
            'comments': 0,
            'counter_lesson': [],
        }
        response = self.client.put(url, self.data, format='multipart')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_delete(self):
        url = reverse('course-detail', args=(self.course1.id,))
        self.data = {
            'id': 3,
            'name': 'test name',
            'course_image': self.file,
            'category': self.category.id,
            'likes': 0,
            'rating': 0,
            'comments': 0,
            'counter_lesson': [],
        }
        response = self.client.delete(url, self.data, format='multipart')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(1, Course.objects.all().count())

