# Generated by Django 4.1 on 2022-09-05 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_account', '0004_delete_userprofile_remove_customuser_activation_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
