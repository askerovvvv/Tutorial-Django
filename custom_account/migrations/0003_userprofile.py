# Generated by Django 4.1 on 2022-09-01 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_account', '0002_remove_customuser_is_teacher'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('date_joined', models.CharField(max_length=100)),
                ('is_active', models.BooleanField()),
                ('is_superuser', models.BooleanField()),
            ],
        ),
    ]
