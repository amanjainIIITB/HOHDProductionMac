# Generated by Django 3.0.5 on 2020-09-27 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0091_auto_20200927_0702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientvisit',
            name='time',
            field=models.TimeField(default='07:03:16'),
        ),
        migrations.AlterField(
            model_name='services',
            name='time',
            field=models.TimeField(default='07:03:16'),
        ),
    ]
