# Generated by Django 3.0.5 on 2020-05-24 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0024_auto_20200524_0805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bharatpe',
            name='time',
            field=models.TimeField(default='16:48:22'),
        ),
        migrations.AlterField(
            model_name='client',
            name='time',
            field=models.TimeField(default='16:48:22'),
        ),
        migrations.AlterField(
            model_name='paytm',
            name='time',
            field=models.TimeField(default='16:48:22'),
        ),
    ]
