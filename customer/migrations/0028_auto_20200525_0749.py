# Generated by Django 3.0.5 on 2020-05-25 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0027_auto_20200525_0740'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bharatpe',
            name='ShopID',
        ),
        migrations.RemoveField(
            model_name='client',
            name='ShopID',
        ),
        migrations.RemoveField(
            model_name='paytm',
            name='ShopID',
        ),
        migrations.AlterField(
            model_name='bharatpe',
            name='time',
            field=models.TimeField(default='07:49:24'),
        ),
        migrations.AlterField(
            model_name='client',
            name='time',
            field=models.TimeField(default='07:49:24'),
        ),
        migrations.AlterField(
            model_name='paytm',
            name='time',
            field=models.TimeField(default='07:49:24'),
        ),
    ]
