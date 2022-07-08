from rest_framework import serializers

from course.models import *


class CourseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseImage
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    courseimage = CourseImageSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES
        course = Course.objects.create(**validated_data)
        for image in images_data.getlist('courseimage'):
            CourseImage.objects.create(course=course, course_image=image)
        return course

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # representation['likes'] = instance.like.filter(like=True).count()

        rating_result = 0
        for i in instance.review.all():
            rating_result += int(i.rating)

        if instance.review.all().count() == 0:
            representation['rating'] = rating_result

        else:
            representation['rating'] = rating_result / instance.review.all().count()

        return representation


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Review
        fields = '__all__'

