# Generated by Django 3.0.5 on 2020-07-31 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0048_auto_20200731_0630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientvisit',
            name='time',
            field=models.TimeField(default='07:05:43'),
        ),
    ]