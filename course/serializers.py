from rest_framework import serializers

from course.models import *
from lesson.serializers import GroupLessonSerializer


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
        representation['counter_lesson'] = GroupLessonSerializer(instance.grouplesson.all(), many=True).data
        return representation


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Review
        fields = '__all__'


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


class CourseRegisterSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = CourseRegister
        fields = ('user', 'course')

    def validate(self, attrs):
        print(attrs.keys())
        user = self.context.get('request').user
        course = attrs.get('course')
        course_from_models = CourseRegister.objects.filter(course=course, user=user)
        print(dir(CourseRegister))
        if course_from_models:
            Course.student_counter = 12
            raise serializers.ValidationError('Вы уже подписаны на данный курс!')
        return attrs

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     instance.course.student_counter += 1
    #     print(instance.course.student_counter)
    #
    #     return representation


class CourseRegisterListSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    course = CourseSerializer(read_only=True)

    class Meta:
        model = CourseRegister
        fields = ('user', 'course')


class SearchHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SearchHistory
        fields = '__all__'
