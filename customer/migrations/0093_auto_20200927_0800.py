# Generated by Django 3.0.5 on 2020-09-27 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0092_auto_20200927_0703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientvisit',
            name='time',
            field=models.TimeField(default='08:00:56'),
        ),
        migrations.AlterField(
            model_name='services',
            name='time',
            field=models.TimeField(default='08:00:56'),
        ),
    ]