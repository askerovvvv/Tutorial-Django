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
    # instance.lesson = LessonSerializer(read_only=True)
    class Meta:
        model = GroupLesson
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['lessons'] = instance.lesson.all().count()

        return representation

