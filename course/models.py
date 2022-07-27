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
    category = models.ForeignKey(Category, related_name='course', on_delete=models.CASCADE, verbose_name='Категория курса')
    course_image = models.ImageField(upload_to='courseimage/', verbose_name='Фото курса')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=None, null=True, blank=True)

    def __str__(self):
        return f'Курс-{self.name}, принадлежит к категории '

    class Meta:
        verbose_name = 'Курс'
        verbose_name = 'Курсы'


class Review(models.Model):
    course = models.ForeignKey(Course, related_name='review', on_delete=models.CASCADE, verbose_name='К какому курсу рейтинг')
    user = models.ForeignKey(User, related_name='review', on_delete=models.CASCADE, verbose_name='Владелец рейтинга')
    description = models.CharField(max_length=300, blank=True, verbose_name='Комментарий')
    rating = models.SmallIntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ])

    def save(self, *args, **kwargs):
        from course.rating_average import set_rating
        creating = not self.pk
        old_rating = self.rating
        super().save(*args, **kwargs)
        new_rating = self.rating
        if old_rating != new_rating or creating:
            set_rating(self.course)

    def __str__(self):
        return f'От пользователя <<{self.user}>> поставлен <<{self.rating}>> к курсу <<{self.course}>>'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Like(models.Model):
    course = models.ForeignKey(Course, related_name='like', on_delete=models.CASCADE, verbose_name='К какому курсу лайк')
    user = models.ForeignKey(User, related_name='like', on_delete=models.CASCADE, verbose_name='Владелец лайка')
    like = models.BooleanField(default=False, verbose_name='Сам лайк')

    def __str__(self):
        return f'От пользователя <<{self.user}>> поставлен <<LIKE>> к курсу <<{self.course}>>'

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'


class SavedCourse(models.Model):
    course = models.ForeignKey(Course, related_name='saved', on_delete=models.CASCADE, verbose_name='Курс для сохранение')
    user = models.ForeignKey(User, related_name='saved', on_delete=models.CASCADE, verbose_name='Пользователь')
    saved = models.BooleanField(default=False, verbose_name='Сохранить')

    def __str__(self):
        if self.saved == True:
            return f"{self.course} --> {self.user}"
        else:
            return f"{self.course} не сохранил"

    class Meta:
        verbose_name = 'Сохраненный курс'
        verbose_name_plural = 'Сохраненные курсы'


class CourseRegister(models.Model):
    course = models.ForeignKey(Course, related_name='courseregister', on_delete=models.CASCADE, verbose_name='К какому курсу')
    user = models.ForeignKey(User, related_name='courseregister', on_delete=models.CASCADE, verbose_name='Какой пользователь')

    def __str__(self):
        return f'{self.user} сохранил курс ---> {self.course}'

    class Meta:
        verbose_name = 'Запись на курс'
        verbose_name_plural = 'Записи на курс'


class SearchHistory(models.Model):
    user = models.ForeignKey(User, related_name='searchhistory', on_delete=models.CASCADE, verbose_name='К какому пользователю принадлежит')
    item = models.CharField(max_length=50, verbose_name='Название для поиска')

    def __str__(self):
        return self.item

    class Meta:
        verbose_name = 'История поиска'
        verbose_name_plural = 'История поиска'

