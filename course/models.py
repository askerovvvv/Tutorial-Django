from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from lesson.models import Lesson

User = get_user_model()


class Category(models.Model):
    """
    Usual Model
    """
    slug = models.SlugField()

    def __str__(self):
        return self.slug

    # class Meta:
    #     verbose_name = 'Категория'
    #     verbose_name_plural = 'Категории'


class Course(models.Model):
    """
    Main model in this project, rating and commen will be filled in automatically by others functions,

    """
    name = models.CharField(max_length=30, verbose_name='Сourse name')
    category = models.ForeignKey(Category, related_name='course', on_delete=models.CASCADE, verbose_name='Сourse category')
    course_image = models.ImageField(upload_to='courseimage/', verbose_name='Сourse photo')
    lessons = models.ManyToManyField(Lesson, related_name='lesson')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0, blank=True)
    comment = models.IntegerField(default=0, blank=True, )
    # adviser = models.ForeignKey(User, related_name='course', on_delete=models.PROTECT)

    def __str__(self):
        return f'Course --> {self.name} '

    # class Meta:
    #     verbose_name = 'Курс'
    #     verbose_name_plural = 'Курсы'


class Review(models.Model):
    """
    Usual model Review, function save for class Course fields comment and rating,
    """
    course = models.ForeignKey(Course, related_name='review', on_delete=models.CASCADE, verbose_name='Which course is rated')
    user = models.ForeignKey(User, related_name='review', on_delete=models.CASCADE, verbose_name='Rating owner')
    description = models.CharField(max_length=300, blank=True, verbose_name='Comment')
    rating = models.SmallIntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ])

    def save(self, *args, **kwargs):
        from course.rating_average import set_rating
        creating = not self.pk
        # old_comment_count = self.description
        old_rating = self.rating
        super().save(*args, **kwargs)
        new_rating = self.rating
        # new_comment_count = self.description
        if old_rating != new_rating or creating:
            set_rating(self.course)
        # if old_comment_count != new_comment_count or creating:
        #     count_comment(self.course)

    def __str__(self):
        return f'<<{self.description}>> by user {self.user}'

    # class Meta:
    #     verbose_name = 'Отзыв'
    #     verbose_name_plural = 'Отзывы'


class Like(models.Model):
    """
    Usual model Like
    """
    course = models.ForeignKey(Course, related_name='like', on_delete=models.CASCADE, verbose_name='Which course is liked')
    user = models.ForeignKey(User, related_name='like', on_delete=models.CASCADE, verbose_name='Like owner')
    like = models.BooleanField(default=False, verbose_name='Like')

    def __str__(self):
        return f'<<{self.course}>> has been liked by <<{self.user}>>'

    # class Meta:
    #     verbose_name = 'Лайк'
    #     verbose_name_plural = 'Лайки'


class SavedCourse(models.Model):
    """
    Usual model SavedCourse
    """
    course = models.ForeignKey(Course, related_name='saved', on_delete=models.CASCADE, verbose_name='Course to save')
    user = models.ForeignKey(User, related_name='saved', on_delete=models.CASCADE, verbose_name='User')
    saved = models.BooleanField(default=False, verbose_name='Save')

    def __str__(self):
        if self.saved == True:
            return f"{self.course} --> {self.user}"
        else:
            return f"{self.course} has not been saved"

    # class Meta:
    #     verbose_name = 'Сохраненный курс'
    #     verbose_name_plural = 'Сохраненные курсы'


class CourseRegister(models.Model):
    """
    Usual model CourseRegister
    """
    course = models.ForeignKey(Course, related_name='courseregister', on_delete=models.CASCADE, verbose_name='Which course')
    user = models.ForeignKey(User, related_name='courseregister', on_delete=models.CASCADE, verbose_name='Which user')

    def __str__(self):
        return f'{self.user} has saved {self.course}'

    # class Meta:
    #     verbose_name = 'Запись на курс'
    #     verbose_name_plural = 'Записи на курс'


class SearchHistory(models.Model):
    """
    Usual model SearchHistory
    """
    user = models.ForeignKey(User, related_name='searchhistory', on_delete=models.CASCADE,)
    item = models.CharField(max_length=50,)

    def __str__(self):
        return self.item
# TODO: история через редис
    class Meta:
        verbose_name = 'Search history --> do not use'
        verbose_name_plural = 'Search history --> do not use'

