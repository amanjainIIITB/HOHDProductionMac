# Generated by Django 3.0.5 on 2020-05-24 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0009_auto_20200520_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateField(default='2020-05-24'),
        ),
    ]