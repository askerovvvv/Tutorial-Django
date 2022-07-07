from rest_framework import serializers

from lesson.models import *


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class AdviserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdviserImage
        fields = '__all__'


class AdviserSerializer(serializers.ModelSerializer):
    adviserimage = AdviserImageSerializer(many=True, read_only=True)

    class Meta:
        model = Adviser
        fields = ('name', 'adviserimage')

    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES
        adviser = Adviser.objects.create(**validated_data)
        for image in images_data.getlist('adviserimage'):
            AdviserImage.objects.create(adviser=adviser, image=image)
        return adviser


    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)


