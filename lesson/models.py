from django.db import models

import course.models


class Adviser(models.Model):
    name = models.CharField(max_length=30, verbose_name='Имя преподавателя')
    course = models.OneToOneField('course.Course', related_name='adviser', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='imageadviser/', verbose_name='Фото преподователя', default=None, blank=True)

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     from course.rating_average import adviser
    #     # creating = not self.pk
    #     # old_rating = self.rating
    #     super().save(*args, **kwargs)
    #     adviser(self.course)

    # new_rating = self.rating
    # if old_rating != new_rating or creating:
    #     set_rating(self.course)
    # if old_comment_count != new_comment_count or creating:
    #     count_comment(self.course)

    class Meta:
        verbose_name = 'Преподователя'
        verbose_name_plural = 'Преподователи'

#
# class GroupLesson(models.Model):
#     name = models.CharField(max_length=50, verbose_name='Название группы уроков')
#     course = models.ForeignKey('course.Course', related_name='grouplesson', on_delete=models.CASCADE, verbose_name='к какому курсу добавить')
#
#     def __str__(self):
#         return f'{self.name} принадлежит к курсу --> {self.course}'
#
#     class Meta:
#         verbose_name = 'Группа уроков'
#         verbose_name_plural = 'Группа уроков'


class Lesson(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название урока')
    description = models.TextField(verbose_name='Описание урока')
    file = models.FileField(upload_to='lessonfile/', verbose_name='Файл с кодом в формате --> MD')
    video = models.FileField(blank=True, upload_to='videolesson/', verbose_name='Усман лапуля')

    def __str__(self):

        return f'{self.name}'


    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'