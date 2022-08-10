from rest_framework import serializers

from course.models import *
from lesson.serializers import LessonSerializer


#
class CategorySerializer(serializers.ModelSerializer):
    """
    Usual ModelSerializer for Category
    """
    class Meta:
        model = Category
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for Course, here used to_representation to get other fields from other classes,
    """
    likes = serializers.IntegerField(read_only=True)
    student_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['lessons'] = instance.lessons.count()
        # print(instance.adviser)
        # representation['adviser'] = instance.
        return representation


class ReviewSerializer(serializers.ModelSerializer):
    """
    Usual Serializer for review, this serializer save user from request
    """
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Review
        fields = '__all__'


class SavedCourseSerializer(serializers.ModelSerializer):
    """
        Usual Serializer for SavedCourse, this serializer shows course that has been saved
    """
    course = CourseSerializer(read_only=True)

    class Meta:
        model = SavedCourse
        fields = ('user', 'course')


class CourseRetrieveSerializer(serializers.ModelSerializer):
    """
    Serializer for Course retrieve request, this serializer shows course with all his description from other users,
    """
    class Meta:
        model = Course
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['comment'] = ReviewSerializer(instance.review.all(), many=True).data
        representation['lessons'] = instance.lessons.count()
        return representation


class CourseRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for CourseRegister, this serializer check if user has already registered to course it will show error
    """
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = CourseRegister
        fields = ('user', 'course')

    def validate(self, attrs):
        user = self.context.get('request').user
        course = attrs.get('course')
        if CourseRegister.objects.filter(user=user, course=course).exists():
            raise serializers.ValidationError('You are already enrolled in this course')

        return attrs


class CourseRegisterListSerializer(serializers.ModelSerializer):
    """
    Serializer for CourseRegister, this serializer for get request it will show course with his lessons
    """
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = CourseRegister
        fields = ('user', 'course')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['course'] = LessonSerializer(instance.course.lessons.all(), many=True).data
        return representation


class SearchHistorySerializer(serializers.ModelSerializer):
    """
    Usual Serializer for SearchHistory
    """
    class Meta:
        model = SearchHistory
        fields = '__all__'
