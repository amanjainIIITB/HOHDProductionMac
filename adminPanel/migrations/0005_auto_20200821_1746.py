# Generated by Django 3.0.5 on 2020-08-21 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminPanel', '0004_auto_20200815_0604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(default='2020-08-21'),
        ),
    ]
