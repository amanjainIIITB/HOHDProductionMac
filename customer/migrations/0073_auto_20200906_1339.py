# Generated by Django 3.0.5 on 2020-09-06 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0072_auto_20200906_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientvisit',
            name='time',
            field=models.TimeField(default='13:39:37'),
        ),
    ]
