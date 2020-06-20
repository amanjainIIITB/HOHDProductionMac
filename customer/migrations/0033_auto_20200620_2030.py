# Generated by Django 3.0.5 on 2020-06-20 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0032_auto_20200620_2014'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='number_of_visit',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='membership',
            name='total_amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='bharatpe',
            name='time',
            field=models.TimeField(default='20:30:27'),
        ),
        migrations.AlterField(
            model_name='client',
            name='time',
            field=models.TimeField(default='20:30:27'),
        ),
        migrations.AlterField(
            model_name='paytm',
            name='time',
            field=models.TimeField(default='20:30:27'),
        ),
    ]
