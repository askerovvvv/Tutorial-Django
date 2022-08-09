from django.db.models import Avg

from course.models import Review, CourseRegister
from lesson.models import Adviser


def set_rating(course):
    rating = Review.objects.filter(course=course).aggregate(rating=Avg('rating')).get('rating')
    course.rating = rating
    course.save()

def count_comment(course):
    comment = Review.objects.filter(course=course, description__exact='').count()
    print(comment)
    if comment:
        print('++++++++++++++++++++++++++++++++++++')
        course.comment += 1
        course.save()

# def adviser(course):
#     adviser_name = Adviser.name
#     print(adviser_name())

# def count_registered_student(course):
#     count_student = CourseRegister.objects.filter(course=course).count()
#     course.registered_student_count = count_student
#     course.save()
