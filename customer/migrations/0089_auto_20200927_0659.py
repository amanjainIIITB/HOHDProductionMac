# Generated by Django 3.0.5 on 2020-09-27 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0088_auto_20200927_0523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientvisit',
            name='time',
            field=models.TimeField(default='06:59:12'),
        ),
        migrations.AlterField(
            model_name='services',
            name='time',
            field=models.TimeField(default='06:59:12'),
        ),
    ]
