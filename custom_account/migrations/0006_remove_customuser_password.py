# Generated by Django 4.1 on 2022-09-05 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_account', '0005_alter_customuser_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='password',
        ),
    ]
