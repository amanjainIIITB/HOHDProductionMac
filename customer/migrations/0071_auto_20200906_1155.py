# Generated by Django 3.0.5 on 2020-09-06 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0070_auto_20200906_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientvisit',
            name='time',
            field=models.TimeField(default='11:55:11'),
        ),
    ]