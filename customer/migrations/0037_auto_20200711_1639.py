# Generated by Django 3.0.5 on 2020-07-11 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0036_auto_20200711_0755'),
    ]

    operations = [
        migrations.AddField(
            model_name='cash',
            name='employee',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='bharatpe',
            name='time',
            field=models.TimeField(default='16:39:15'),
        ),
        migrations.AlterField(
            model_name='cash',
            name='time',
            field=models.TimeField(default='16:39:15'),
        ),
        migrations.AlterField(
            model_name='paytm',
            name='time',
            field=models.TimeField(default='16:39:15'),
        ),
    ]
