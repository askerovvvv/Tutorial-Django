from rest_framework import serializers

from course.models import *


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes'] = instance.like.filter(like=True).count()
        rating_result = 0
        sum_of_description = 0
        for i in instance.review.all():
            rating_result += int(i.rating)
            if i.description:
                sum_of_description += 1
        if instance.review.all().count() == 0:
            representation['rating'] = rating_result

        else:
            representation['rating'] = rating_result / instance.review.all().count()
        representation['comments'] = sum_of_description
        return representation


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Review
        fields = ('user', 'description', 'rating')


class SavedCourseSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = SavedCourse
        fields = ('user', 'course')


class CourseRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['Отзывы'] = ReviewSerializer(instance.review.all(), many=True).data
        return representation