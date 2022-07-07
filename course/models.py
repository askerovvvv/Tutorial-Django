from django.db import models

from lesson.models import Adviser


class Category(models.Model):
    slug = models.SlugField()


class Course(models.Model):
    name = models.CharField(max_length=30)
    # student_counter
    category = models.ForeignKey(Category, related_name='course', on_delete=models.CASCADE)
    adviser = models.ForeignKey(Adviser, related_name='course', on_delete=models.CASCADE)
