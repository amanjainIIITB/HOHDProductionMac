# Generated by Django 3.0.5 on 2020-10-11 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0096_auto_20201011_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientvisit',
            name='time',
            field=models.TimeField(default='17:47:56'),
        ),
        migrations.AlterField(
            model_name='services',
            name='time',
            field=models.TimeField(default='17:47:56'),
        ),
    ]
