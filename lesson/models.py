from django.db import models

import course.models


class Adviser(models.Model):
    name = models.CharField(max_length=30, verbose_name='Имя преподавателя')
    course = models.ForeignKey('course.Course', related_name='adviser', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='imageadviser/', verbose_name='Фото преподователя')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Преподователя'
        verbose_name_plural = 'Преподователи'


class GroupLesson(models.Model):
    name = models.CharField(max_length=50)
    course = models.ForeignKey('course.Course', related_name='grouplesson', on_delete=models.CASCADE)


class Lesson(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название урока')
    description = models.TextField(verbose_name='Описание урока')
    file = models.FileField(upload_to='lessonfile/', verbose_name='Файл с кодом в формате --> MD')
    # course = models.ForeignKey('course.Course', related_name='lesson', on_delete=models.CASCADE, verbose_name='К какому курсу добавить урок')
    video = models.FileField(blank=True, upload_to='videolesson/', verbose_name='Усман лапуля')
    group_lesson = models.ForeignKey(GroupLesson, related_name='lesson', on_delete=models.CASCADE)

    def __str__(self):
        if not self.video:
            return f'Урок-{self.name} для  --> {self.group_lesson}'
        else:
            return f'Урок-{self.name} для  --> {self.group_lesson} <<ИМЕЕТСЯ ВИДЕО>>'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'