# Generated by Django 4.0.6 on 2022-07-28 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_course_lessons'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='comment',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
