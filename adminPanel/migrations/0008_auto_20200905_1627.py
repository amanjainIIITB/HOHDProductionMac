# Generated by Django 3.0.5 on 2020-09-05 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminPanel', '0007_auto_20200904_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(default='2020-09-05'),
        ),
    ]
