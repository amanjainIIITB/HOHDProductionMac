# Generated by Django 3.0.5 on 2020-09-27 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0004_auto_20200920_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='date',
            field=models.DateField(default='2020-09-27'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='date_of_joining',
            field=models.DateField(default='2020-09-27'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateField(default='2020-09-27'),
        ),
    ]