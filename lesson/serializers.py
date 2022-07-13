from rest_framework import serializers

from lesson.models import *


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class AdviserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adviser
        fields = '__all__'


class GroupLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupLesson
        fields = '__all__'

