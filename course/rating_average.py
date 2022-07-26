from django.db.models import Avg

from course.models import Review


def set_rating(course):
    rating = Review.objects.filter(course=course).aggregate(rating=Avg('rating')).get('rating')
    course.rating = rating
    course.save()

