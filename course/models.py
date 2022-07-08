from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from lesson.models import Adviser
User = get_user_model()


class Category(models.Model):
    slug = models.SlugField()

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = 'Категория'
        verbose_name = 'Категории'


class Course(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название курса')
    # student_counter
    category = models.ForeignKey(Category, related_name='course', on_delete=models.CASCADE, verbose_name='Категория курса')

    def __str__(self):
        return f'Курс-{self.name}, принадлежит к категории {self.category}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name = 'Курсы'


class CourseImage(models.Model):
    course = models.ForeignKey(Course, related_name='courseimage', on_delete=models.CASCADE, verbose_name='К какому курсу принадлежит')
    course_image = models.ImageField(upload_to='courseimage/', verbose_name='Фото курса')

    def __str__(self):
        return f'Это фото для курса {self.course}'

    class Meta:
        verbose_name = 'Фото курса'
        verbose_name_plural = 'Фото курсов'


class Review(models.Model):
    course = models.ForeignKey(Course, related_name='review', on_delete=models.CASCADE, verbose_name='К какому курсу рейтинг')
    user = models.ForeignKey(User, related_name='review', on_delete=models.CASCADE, verbose_name='Владелец рейтинга')
    description = models.CharField(max_length=300, blank=True, verbose_name='Комментарий')
    rating = models.SmallIntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ])

    def __str__(self):
        return f'От пользователя <<{self.user}>> поставлен <<{self.rating}>> к курсу <<{self.course}>>'

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Like(models.Model):
    course = models.ForeignKey(Course, related_name='like', on_delete=models.CASCADE, verbose_name='К какому курсу лайк')
    user = models.ForeignKey(User, related_name='like', on_delete=models.CASCADE, verbose_name='Владелец лайка')
    like = models.BooleanField(default=False, verbose_name='Сам лайк')

    def __str__(self):
        return f'От пользователя <<{self.user}>> поставлен <<LIKE>> к курсу <<{self.course}>>'

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
