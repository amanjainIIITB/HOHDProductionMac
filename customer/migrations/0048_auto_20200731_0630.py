# Generated by Django 3.0.5 on 2020-07-31 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0047_auto_20200726_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientvisit',
            name='bardate',
            field=models.DateField(default='2020-07-31'),
        ),
        migrations.AlterField(
            model_name='clientvisit',
            name='date',
            field=models.DateField(default='2020-07-31'),
        ),
        migrations.AlterField(
            model_name='clientvisit',
            name='time',
            field=models.TimeField(default='06:30:47'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='DOB',
            field=models.DateField(default='2020-07-31'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='last_visit',
            field=models.DateField(default='2020-07-31'),
        ),
    ]
