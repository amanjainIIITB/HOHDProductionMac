# Generated by Django 3.0.5 on 2020-05-01 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0007_auto_20200501_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bharatpe',
            name='time',
            field=models.TimeField(default='13:06:56'),
        ),
        migrations.AlterField(
            model_name='client',
            name='time',
            field=models.TimeField(default='13:06:56'),
        ),
        migrations.AlterField(
            model_name='paytm',
            name='time',
            field=models.TimeField(default='13:06:56'),
        ),
    ]