# Generated by Django 3.0.5 on 2020-10-11 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0094_auto_20201011_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientvisit',
            name='time',
            field=models.TimeField(default='11:35:13'),
        ),
        migrations.AlterField(
            model_name='services',
            name='time',
            field=models.TimeField(default='11:35:13'),
        ),
    ]
