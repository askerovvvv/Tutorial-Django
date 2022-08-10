from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from course.permission import IsTeacherUser
from lesson.models import *
from lesson.serializers import *
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class LessonViewSet(ModelViewSet):
    """
    Ussual viewset for crud for the model Lesson
    """
    permission_classes = [IsTeacherUser]
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


# class AdviserViewSet(ModelViewSet):
#     """
#     Ussual viewset for crud for the model Adviser, but to create adviser user must be superuser
#     """
#     queryset = Adviser.objects.all()
#     serializer_class = AdviserSerializer
#
#     def get_permissions(self):
#         if self.action in ['list', 'retrieve']:
#             permissions = [IsAuthenticated]
#         else:
#             permissions = [IsAdminUser]
#
#         return [permission() for permission in permissions]
#

# class GroupLessonViewSet(ModelViewSet):
#     queryset = GroupLesson.objects.all()
#     serializer_class = GroupLessonSerializer