# Generated by Django 4.0.6 on 2022-07-28 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adviser',
            name='image',
            field=models.ImageField(blank=True, default=None, upload_to='imageadviser/', verbose_name='Фото преподователя'),
        ),
    ]
