# Generated by Django 4.1 on 2022-09-05 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_account', '0008_alter_customuser_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='activation_code',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(max_length=100),
        ),
    ]
