# Generated by Django 4.1 on 2022-08-09 07:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0001_initial'),
        ('lesson', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchhistory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='searchhistory', to=settings.AUTH_USER_MODEL, verbose_name='К какому пользователю принадлежит'),
        ),
        migrations.AddField(
            model_name='savedcourse',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved', to='course.course', verbose_name='Курс для сохранение'),
        ),
        migrations.AddField(
            model_name='savedcourse',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='review',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to='course.course', verbose_name='К какому курсу рейтинг'),
        ),
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to=settings.AUTH_USER_MODEL, verbose_name='Владелец рейтинга'),
        ),
        migrations.AddField(
            model_name='like',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like', to='course.course', verbose_name='К какому курсу лайк'),
        ),
        migrations.AddField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like', to=settings.AUTH_USER_MODEL, verbose_name='Владелец лайка'),
        ),
        migrations.AddField(
            model_name='courseregister',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courseregister', to='course.course', verbose_name='К какому курсу'),
        ),
        migrations.AddField(
            model_name='courseregister',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courseregister', to=settings.AUTH_USER_MODEL, verbose_name='Какой пользователь'),
        ),
        migrations.AddField(
            model_name='course',
            name='adviser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='course', to='lesson.adviser'),
        ),
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course', to='course.category', verbose_name='Категория курса'),
        ),
        migrations.AddField(
            model_name='course',
            name='lessons',
            field=models.ManyToManyField(related_name='lesson', to='lesson.lesson'),
        ),
    ]
