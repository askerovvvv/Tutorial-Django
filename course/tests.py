import io

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from django.db.models import Count, Case, When
from rest_framework import status
from PIL import Image

from rest_framework.test import APITestCase

from django.urls import reverse
from course.models import Course, Category, Review
from course.rating_average import set_rating
from course.serializers import CourseSerializer, ReviewSerializer

import json

from lesson.models import Lesson

User = get_user_model()


class CourseTestApiCase(APITestCase):
    """
    crud test for Course
    """
    def setUp(self):
        self.category = Category.objects.create(slug='Programming')
        self.lesson1 = Lesson.objects.create(name='lesson1', )
        self.user = User.objects.create(email='testsuperuser@gmail.com', is_staff=True)
        self.user2 = User.objects.create(email='testuser@gmail.com')
        # self.adviser1 = Adviser.objects.create(name='Adviser1',)
        # self.adviser2 = Adviser.objects.create(name='Adviser2',)
        self.course1 = Course.objects.create(name='Python', category=self.category, )
        self.course2 = Course.objects.create(name='JS', category=self.category,)
        course = Course.objects.all().annotate(student_count=Count('courseregister'), likes=Count(Case(When(like__like=True, then=1)))).prefetch_related('lessons')

        self.serializer_data = CourseSerializer(course, many=True).data
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
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # self.assertEqual(self.serializer_data, response.data)
        self.assertEqual(len(self.serializer_data), len(response.data))

    def test_post(self):
        url = reverse('course-list')
        self.data = {
            'id': 3,
            'name': 'Java',
            'course_image': self.file,
            'category': self.category.id,
            'lessons': self.lesson1.id,
            'rating': 0,
            'comment': 0,
            # 'adviser': self.adviser1.id
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, self.data, format='multipart')
        print(response.json())
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # self.assertTrue(f'media/courseimage/image_mryWGaN.jpg' in response.data['course_image'])
        self.assertEqual(3, Course.objects.all().count())

    def test_invalid_post(self):
        url = reverse('course-list')
        self.data = {
            'id': 3,
            'name': 'Java',
            'course_image': self.file,
            'category': self.category.id,
            'lessons': self.lesson1.id,
            'rating': 0,
            'comment': 0,
            # 'adviser': self.adviser1.id
        }
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(url, self.data, format='multipart')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        # self.assertTrue(f'media/courseimage/image_mryWGaN.jpg' in response.data['course_image'])
        self.assertTrue(2 == Course.objects.all().count())

    def test_update(self):
        url = reverse('course-detail', args=(self.course1.id,))
        self.data = {
            'id': 3,
            'name': 'test name',
            'course_image': self.file,
            'category': self.category.id,
            'lessons': self.lesson1.id,
            'rating': 0,
            'comment': 0,
            # 'adviser': self.adviser1.id
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, self.data, format='multipart')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.course1.refresh_from_db()
        self.assertEqual('test name', self.course1.name)

    def test_invalid_update(self):
        url = reverse('course-detail', args=(self.course1.id,))
        self.data = {
            'id': 3,
            'name': 'Java',
            'course_image': self.file,
            'category': self.category.id,
            'lessons': self.lesson1.id,
            'rating': 0,
            'comment': 0,
            # 'adviser': self.adviser1.id
        }
        self.client.force_authenticate(user=self.user2)
        response = self.client.put(url, self.data, format='multipart')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        ######################
        ########################

    def test_delete(self):
        url = reverse('course-detail', args=(self.course1.id,))
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url, )
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(1, Course.objects.all().count())

    def test_invalid_delete(self):
        url = reverse('course-detail', args=(self.course1.id,))
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(url, )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertTrue(2 == Course.objects.all().count())


class ReviewTestApiCase(APITestCase):
    """
    Crud test for Review
    """
    def setUp(self):
        self.category = Category.objects.create(slug='Programming')
        # self.adviser1 = Adviser.objects.create(name='Adviser1', )
        self.course = Course.objects.create(name='Python', category=self.category,)
        self.user = User.objects.create_user(email='test1@gmail.com', password='123345631')
        self.user2 = User.objects.create_user(email='test2@gmail.com', password='4124132')
        self.review1 = Review.objects.create(course=self.course, user=self.user, description='testreview1,', rating=5)
        self.review2 = Review.objects.create(course=self.course, user=self.user2, description='rqwfq,', rating=3)
        self.serializer_data = ReviewSerializer(Review.objects.all(), many=True).data
        # self.adviser2 = Adviser.objects.create(name='Adviser2', )

    def test_ok(self):
        set_rating(self.course)
        self.course.refresh_from_db()
        self.assertEqual('4.00', str(self.course.rating))

    def test_get(self):
        url = reverse('review-list')
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(url)
        # print('+++++++++++++++++++++++++++++++++')
        # print(self.serializer_data,)
        # print(response.data[0][0])
        # print(response)
        #
        # self.assertEqual(Review.objects.filter(user=self.user2).get(self.user2), self.user2)
        self.assertEqual(Review.objects.all().count(), len(self.serializer_data))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_post(self):
        url = reverse('review-list')
        authenticated_user = self.client.force_authenticate(user=self.user2)
        data = {
            'id': 3,
            'course': self.course.id,
            'user': authenticated_user,
            'description': 'posttest',
            'rating': 4
        }
        json_data = json.dumps(data)
        response = self.client.post(url, json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(Review.objects.all().count(), 3)

    def test_invalid_post_without_authentication(self):
        url = reverse('review-list')
        data = {
            'id': 3,
            'course': self.course.id,
            'user': self.user.id,
            'description': 'posttest',
            'rating': 4
        }
        json_data = json.dumps(data)
        response = self.client.post(url, json_data, content_type='application/json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual(Review.objects.all().count(), 2)

    def test_invalid_rating_post(self):
        url = reverse('review-list')
        authenticated_user = self.client.force_authenticate(user=self.user2)
        data = {
            'id': 3,
            'course': self.course.id,
            'user': authenticated_user,
            'description': 'posttest',
            'rating': 6
        }
        json_data = json.dumps(data)
        response = self.client.post(url, json_data, content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(Review.objects.all().count(), 2)

    # def test_update(self):
    #     url = reverse('review-detail', args=(self.review1.id,))
    #     print(url)
    #     self.client.force_authenticate(user=self.user2)
    #     data = {
    #         'id': 3,
    #         'course': self.course.id,
    #         'user': self.user2,
    #         'description': 'update test',
    #         'rating': 3
    #     }
    #     response = self.client.put(url, data,)
    #     self.assertEqual(status.HTTP_200_OK, response.status_code)
    #

    # def test_delete(self):
    #     url = reverse('review-detail', args=(self.review1.id,))
    #
    #
