# Generated by Django 3.0.5 on 2020-10-11 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminPanel', '0012_auto_20200927_0430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(default='2020-10-11'),
        ),
    ]