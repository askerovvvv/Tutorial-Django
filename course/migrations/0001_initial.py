# Generated by Django 4.1.1 on 2022-09-07 03:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("slug", models.SlugField()),
            ],
            options={
                "verbose_name": "Категория",
                "verbose_name_plural": "Категории",
            },
        ),
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=30, verbose_name="Название курса"),
                ),
                (
                    "course_image",
                    models.ImageField(
                        upload_to="courseimage/", verbose_name="Фото курса"
                    ),
                ),
                (
                    "rating",
                    models.DecimalField(
                        blank=True, decimal_places=2, default=0, max_digits=3
                    ),
                ),
                ("comment", models.IntegerField(blank=True, default=0)),
            ],
            options={
                "verbose_name": "Курс",
                "verbose_name_plural": "Курсы",
            },
        ),
        migrations.CreateModel(
            name="CourseRegister",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "verbose_name": "Запись на курс",
                "verbose_name_plural": "Записи на курс",
            },
        ),
        migrations.CreateModel(
            name="Like",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("like", models.BooleanField(default=False, verbose_name="Сам лайк")),
            ],
            options={
                "verbose_name": "Лайк",
                "verbose_name_plural": "Лайки",
            },
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True, max_length=300, verbose_name="Комментарий"
                    ),
                ),
                (
                    "rating",
                    models.SmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5),
                        ]
                    ),
                ),
            ],
            options={
                "verbose_name": "Отзыв",
                "verbose_name_plural": "Отзывы",
            },
        ),
        migrations.CreateModel(
            name="SavedCourse",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("saved", models.BooleanField(default=False, verbose_name="Сохранить")),
            ],
            options={
                "verbose_name": "Сохраненный курс",
                "verbose_name_plural": "Сохраненные курсы",
            },
        ),
        migrations.CreateModel(
            name="SearchHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "item",
                    models.CharField(max_length=50, verbose_name="Название для поиска"),
                ),
            ],
            options={
                "verbose_name": "История поиска",
                "verbose_name_plural": "История поиска",
            },
        ),
    ]
