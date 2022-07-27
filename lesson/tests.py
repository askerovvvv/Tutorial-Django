import io

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from course.models import Course, Category
from lesson.models import GroupLesson, Lesson
from lesson.serializers import LessonSerializer
from django.urls import reverse
from rest_framework import status
User = get_user_model()

class LessonTestApiCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('testlesson@gmail.com', password='123456', is_staff=True)
        self.user2 = User.objects.create_user('testuser@gmail.com', password='123456', is_staff=False)
        self.category = Category.objects.create(slug='Programming')
        self.course = Course.objects.create(name='Python', category=self.category)
        self.grouplesson = GroupLesson.objects.create(name='1', course=self.course)
        self.lesson1 = Lesson.objects.create(name='testlesson1', description='testdescription1', group_lesson=self.grouplesson)
        self.lesson2 = Lesson.objects.create(name='testlesson1', description='testdescription1', group_lesson=self.grouplesson)
        self.serializer_data = LessonSerializer(Lesson.objects.all(), many=True).data

        self.file_md = SimpleUploadedFile(
            "best_file_eva.md",
            b"these are the file contents!"  # note the b in front of the string [bytes]
        )
        self.video_file = SimpleUploadedFile(
            "file_video.mp4",
            b"these are the file contents!"  # note the b in front of the string [bytes]
        )

    def test_get(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('lesson-list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.serializer_data, response.data)
        self.assertEqual(Lesson.objects.all().count(), len(response.data))

        # file = io.BytesIO()
        # Image.new('RGB', (150, 150)).save(image, 'JPEG')
        # image.seek(0)
        # self.file = SimpleUploadedFile('image.jpg', image.getvalue())


    def test_invalid_get_without_admin_user(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('lesson-list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_post(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('lesson-list')
        data = {
            'name': 'Test post 1',
            'description': 'description for post request',
            'file': self.file_md,
            'video': self.video_file,
            'group_lesson': self.grouplesson.id
        }

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # self.assertTrue(f'media/lessonfile/best_file_eva_U19Km8t.md'' in response.data['file'])
        self.assertEqual(3, Lesson.objects.all().count())

    def test_valid_post_without_video(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('lesson-list')
        data = {
            'name': 'Test post 1',
            'description': 'description for post request',
            'file': self.file_md,
            'group_lesson': self.grouplesson.id
        }

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # self.assertTrue(f'media/lessonfile/best_file_eva_U19Km8t.md'' in response.data['file'])
        self.assertEqual(3, Lesson.objects.all().count())

    def test_invalid_post_without_admin_user(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('lesson-list')
        data = {
            'name': 'Test post 1',
            'description': 'description for post request',
            'file': self.file_md,
            'video': self.video_file,
            'group_lesson': self.grouplesson.id
        }

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        # self.assertTrue(f'media/lessonfile/best_file_eva_U19Km8t.md'' in response.data['file'])
        self.assertEqual(2, Lesson.objects.all().count())

    def test_invalid_post_without_authenticate(self):
        url = reverse('lesson-list')
        data = {
            'name': 'Test post 1',
            'description': 'description for post request',
            'file': self.file_md,
            'video': self.video_file,
            'group_lesson': self.grouplesson.id
        }

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        # self.assertTrue(f'media/lessonfile/best_file_eva_U19Km8t.md'' in response.data['file'])
        self.assertEqual(2, Lesson.objects.all().count())

    def test_update(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('lesson-detail', args=(self.lesson1.id,))
        data = {
            'name': 'TEst name after UPDATE',
            'description': 'description AFTER UPDATE',
            'file': self.file_md,
            'video': self.video_file,
            'group_lesson': self.grouplesson.id
        }

        response = self.client.put(url, data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, Lesson.objects.all().count())
        self.lesson1.refresh_from_db()
        self.assertEqual('TEst name after UPDATE', self.lesson1.name)
        self.assertEqual('description AFTER UPDATE', self.lesson1.description)

    def test_invalid_update_without_admin_user(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('lesson-detail', args=(self.lesson1.id,))
        data = {
            'name': 'TEst name after UPDATE',
            'description': 'description AFTER UPDATE',
            'file': self.file_md,
            'video': self.video_file,
            'group_lesson': self.grouplesson.id
        }

        response = self.client.put(url, data)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.lesson1.refresh_from_db()
        self.assertEqual('testlesson1', self.lesson1.name)
        self.assertEqual('testdescription1', self.lesson1.description)

    def test_invalid_update_without_authenticate(self):
        url = reverse('lesson-detail', args=(self.lesson1.id,))
        data = {
            'name': 'TEst name after UPDATE',
            'description': 'description AFTER UPDATE',
            'file': self.file_md,
            'video': self.video_file,
            'group_lesson': self.grouplesson.id
        }

        response = self.client.put(url, data)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.lesson1.refresh_from_db()
        self.assertEqual('testlesson1', self.lesson1.name)
        self.assertEqual('testdescription1', self.lesson1.description)

    def test_delete(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('lesson-detail', args=(self.lesson1.id,))
        response = self.client.delete(url, )
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(Lesson.objects.all().count(), 1)

    def test_invalid_delete_without_admin_user(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('lesson-detail', args=(self.lesson1.id,))
        response = self.client.delete(url, )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_invalid_delete_without_authenticate(self):
        url = reverse('lesson-detail', args=(self.lesson1.id,))
        response = self.client.delete(url, )
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual(Lesson.objects.all().count(), 2)





