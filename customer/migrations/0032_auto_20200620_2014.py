# Generated by Django 3.0.5 on 2020-06-20 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0031_auto_20200620_0845'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='last_visit',
            field=models.DateField(default='2020-06-20'),
        ),
        migrations.AlterField(
            model_name='bharatpe',
            name='time',
            field=models.TimeField(default='20:14:57'),
        ),
        migrations.AlterField(
            model_name='client',
            name='time',
            field=models.TimeField(default='20:14:56'),
        ),
        migrations.AlterField(
            model_name='paytm',
            name='time',
            field=models.TimeField(default='20:14:57'),
        ),
    ]
