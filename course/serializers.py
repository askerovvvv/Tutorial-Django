from rest_framework import serializers

from course.models import *
from lesson.serializers import AdviserSerializer, LessonSerializer


#
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    # course_image = serializers.ListField(child=serializers.ImageField(
    #     max_length=10000, allow_empty_file=False), write_only=True,
    #     min_length=1, max_length=5)
    likes = serializers.IntegerField(read_only=True)
    # lessons = serializers.SerializerMethodField(read_only=True)
    student_count = serializers.IntegerField(read_only=True)
    # adviser = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
    #
    # def get_adviser(self, instance):
    #     return AdviserSerializer(instance.adviser, ).data

    def to_representation(self, instance):
        # representation['lessons'] = instance.les
        representation = super().to_representation(instance)
        # sum_of_description = 0
        #
        # for i in instance.review.all():
        #     #     rating_result += int(i.rating)
        #     if i.description:
                # sum_of_description += 1
        #     # print(instance.review.filter(description='!=null'))
        #
        # representation['comments'] = sum_of_description
        representation['lessons'] = instance.lessons.count()
        representation['adviser'] = AdviserSerializer(instance.adviser,).data
        print(instance.adviser)
        return representation

    #     sum_of_description = 0
    #
    #     for i in instance.review.all():
    #     #     rating_result += int(i.rating)
    #         if i.description:
    #             sum_of_description += 1
    #     # print(instance.review.filter(description='!=null'))
    #
    #     representation['comments'] = sum_of_description
    #     # representation['counter_lesson'] = GroupLessonSerializer(instance.grouplesson.all(), many=True).data
    #     representation['saved_counter'] = instance.saved.count()
    #     representation['register_counter'] = instance.courseregister.count()
    #     representation['adviser'] = AdviserSerializer(instance.adviser.all(), many=True).data
    #     return representation


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
        representation['comment'] = ReviewSerializer(instance.review.all(), many=True).data
        representation['lessons'] = instance.lessons.count()
        return representation


class CourseRegisterSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = CourseRegister
        fields = ('user', 'course')

    def validate(self, attrs):
        user = self.context.get('request').user
        course = attrs.get('course')
        if CourseRegister.objects.filter(user=user, course=course).exists():
            raise serializers.ValidationError('Вы уже записаны на данный курс')

        return attrs


class CourseRegisterListSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    # course = CourseSerializer(read_only=True)
    # course = serializers.SerializerMethodField

    class Meta:
        model = CourseRegister
        fields = ('user', 'course')

    # def get_course(self):
    #     print(CourseRegister)
    #     return (CourseRegister.user)
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['course'] = LessonSerializer(instance.course.lessons.all(), many=True).data
        return representation

class SearchHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SearchHistory
        fields = '__all__'
