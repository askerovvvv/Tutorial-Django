from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from lesson.models import *
from lesson.serializers import *


class LessonViewSet(ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class AdviserViewSet(ModelViewSet):
    queryset = Adviser.objects.all()
    serializer_class = AdviserSerializer
