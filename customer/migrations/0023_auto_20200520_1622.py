# Generated by Django 3.0.5 on 2020-05-20 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0022_auto_20200519_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bharatpe',
            name='bardate',
            field=models.DateField(default='2020-05-20'),
        ),
        migrations.AlterField(
            model_name='bharatpe',
            name='date',
            field=models.DateField(default='2020-05-20'),
        ),
        migrations.AlterField(
            model_name='bharatpe',
            name='time',
            field=models.TimeField(default='16:22:44'),
        ),
        migrations.AlterField(
            model_name='client',
            name='bardate',
            field=models.DateField(default='2020-05-20'),
        ),
        migrations.AlterField(
            model_name='client',
            name='date',
            field=models.DateField(default='2020-05-20'),
        ),
        migrations.AlterField(
            model_name='client',
            name='time',
            field=models.TimeField(default='16:22:44'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='DOB',
            field=models.DateField(default='2020-05-20'),
        ),
        migrations.AlterField(
            model_name='paytm',
            name='bardate',
            field=models.DateField(default='2020-05-20'),
        ),
        migrations.AlterField(
            model_name='paytm',
            name='date',
            field=models.DateField(default='2020-05-20'),
        ),
        migrations.AlterField(
            model_name='paytm',
            name='time',
            field=models.TimeField(default='16:22:44'),
        ),
    ]