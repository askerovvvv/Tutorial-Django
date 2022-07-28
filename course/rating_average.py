from django.db.models import Avg

from course.models import Review


def set_rating(course):
    rating = Review.objects.filter(course=course).aggregate(rating=Avg('rating')).get('rating')
    course.rating = rating
    course.save()

def count_comment(course):
    comment = Review.objects.filter(course=course, description__isnull=False).exists()
    if comment:
        course.comment += 1
        course.save()