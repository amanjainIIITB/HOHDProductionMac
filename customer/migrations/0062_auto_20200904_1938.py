# Generated by Django 3.0.5 on 2020-09-04 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0061_auto_20200904_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientvisit',
            name='date',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='clientvisit',
            name='time',
            field=models.TimeField(default='19:38:53'),
        ),
    ]
