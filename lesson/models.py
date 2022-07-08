from django.db import models

import course.models


class Adviser(models.Model):
    name = models.CharField(max_length=30, verbose_name='Имя преподавателя')
    course = models.ForeignKey('course.Course', related_name='adviser', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Преподователя'
        verbose_name_plural = 'Преподователи'


class AdviserImage(models.Model):
    adviser = models.ForeignKey(Adviser, related_name='adviserimage', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='adviserimage', verbose_name='Фото преподователя')


class Lesson(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название урока')
    description = models.TextField(verbose_name='Описание урока')
    file = models.FileField(upload_to='lessonfile/', verbose_name='Файл с кодом в формате --> MD')
    course = models.ForeignKey('course.Course', related_name='lesson', on_delete=models.CASCADE, verbose_name='К какому курсу добавить урок')

    def __str__(self):
        return f'Урок-{self.name} для курса --> {self.course}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Video(models.Model):
    video = models.FileField(upload_to='videolesson/', verbose_name='Усман лапуля')
    lesson = models.ForeignKey(Lesson, related_name='video', on_delete=models.CASCADE, verbose_name='Видео для урока')

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'
