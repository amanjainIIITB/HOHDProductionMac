# Generated by Django 3.0.5 on 2020-09-27 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0087_auto_20200927_0515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientvisit',
            name='time',
            field=models.TimeField(default='05:23:49'),
        ),
        migrations.AlterField(
            model_name='services',
            name='time',
            field=models.TimeField(default='05:23:49'),
        ),
    ]