# Generated by Django 3.0.5 on 2020-09-06 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0067_auto_20200906_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientvisit',
            name='time',
            field=models.TimeField(default='11:46:40'),
        ),
    ]
