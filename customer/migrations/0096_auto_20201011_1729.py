# Generated by Django 3.0.5 on 2020-10-11 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0095_auto_20201011_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientvisit',
            name='time',
            field=models.TimeField(default='17:28:59'),
        ),
        migrations.AlterField(
            model_name='services',
            name='time',
            field=models.TimeField(default='17:28:59'),
        ),
    ]
