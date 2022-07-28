# Generated by Django 4.0.6 on 2022-07-28 16:12

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lesson', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField()),
            ],
            options={
                'verbose_name': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Название курса')),
                ('course_image', models.ImageField(upload_to='courseimage/', verbose_name='Фото курса')),
                ('rating', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=3, null=True)),
                ('comment', models.IntegerField(blank=True, default=None, null=True)),
                ('adviser_name', models.CharField(blank=True, max_length=30, null=True)),
                ('adviser_image', models.ImageField(blank=True, default=None, upload_to='imageadviser/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course', to='course.category', verbose_name='Категория курса')),
                ('lessons', models.ManyToManyField(related_name='lesson', to='lesson.lesson')),
            ],
            options={
                'verbose_name': 'Курс',
                'verbose_name_plural': 'Курсы',
            },
        ),
        migrations.CreateModel(
            name='SearchHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=50, verbose_name='Название для поиска')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='searchhistory', to=settings.AUTH_USER_MODEL, verbose_name='К какому пользователю принадлежит')),
            ],
            options={
                'verbose_name': 'История поиска',
                'verbose_name_plural': 'История поиска',
            },
        ),
        migrations.CreateModel(
            name='SavedCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saved', models.BooleanField(default=False, verbose_name='Сохранить')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved', to='course.course', verbose_name='Курс для сохранение')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Сохраненный курс',
                'verbose_name_plural': 'Сохраненные курсы',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=300, verbose_name='Комментарий')),
                ('rating', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to='course.course', verbose_name='К какому курсу рейтинг')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to=settings.AUTH_USER_MODEL, verbose_name='Владелец рейтинга')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False, verbose_name='Сам лайк')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like', to='course.course', verbose_name='К какому курсу лайк')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like', to=settings.AUTH_USER_MODEL, verbose_name='Владелец лайка')),
            ],
            options={
                'verbose_name': 'Лайк',
                'verbose_name_plural': 'Лайки',
            },
        ),
        migrations.CreateModel(
            name='CourseRegister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courseregister', to='course.course', verbose_name='К какому курсу')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courseregister', to=settings.AUTH_USER_MODEL, verbose_name='Какой пользователь')),
            ],
            options={
                'verbose_name': 'Запись на курс',
                'verbose_name_plural': 'Записи на курс',
            },
        ),
    ]
