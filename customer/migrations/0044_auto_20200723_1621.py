# Generated by Django 3.0.5 on 2020-07-23 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0043_auto_20200721_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientvisit',
            name='bardate',
            field=models.DateField(default='2020-07-23'),
        ),
        migrations.AlterField(
            model_name='clientvisit',
            name='date',
            field=models.DateField(default='2020-07-23'),
        ),
        migrations.AlterField(
            model_name='clientvisit',
            name='time',
            field=models.TimeField(default='16:21:48'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='DOB',
            field=models.DateField(default='2020-07-23'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='last_visit',
            field=models.DateField(default='2020-07-23'),
        ),
    ]
