# Generated by Django 3.0.5 on 2020-05-02 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0013_auto_20200502_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bharatpe',
            name='time',
            field=models.TimeField(default='11:22:43'),
        ),
        migrations.AlterField(
            model_name='client',
            name='time',
            field=models.TimeField(default='11:22:43'),
        ),
        migrations.AlterField(
            model_name='paytm',
            name='time',
            field=models.TimeField(default='11:22:43'),
        ),
    ]
