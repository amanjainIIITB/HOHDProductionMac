# Generated by Django 3.0.5 on 2020-05-01 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0009_auto_20200501_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bharatpe',
            name='time',
            field=models.TimeField(default='14:33:51'),
        ),
        migrations.AlterField(
            model_name='client',
            name='time',
            field=models.TimeField(default='14:33:51'),
        ),
        migrations.AlterField(
            model_name='paytm',
            name='time',
            field=models.TimeField(default='14:33:51'),
        ),
    ]