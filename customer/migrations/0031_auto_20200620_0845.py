# Generated by Django 3.0.5 on 2020-06-20 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0030_auto_20200607_0435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bharatpe',
            name='bardate',
            field=models.DateField(default='2020-06-20'),
        ),
        migrations.AlterField(
            model_name='bharatpe',
            name='date',
            field=models.DateField(default='2020-06-20'),
        ),
        migrations.AlterField(
            model_name='bharatpe',
            name='time',
            field=models.TimeField(default='08:45:09'),
        ),
        migrations.AlterField(
            model_name='client',
            name='bardate',
            field=models.DateField(default='2020-06-20'),
        ),
        migrations.AlterField(
            model_name='client',
            name='date',
            field=models.DateField(default='2020-06-20'),
        ),
        migrations.AlterField(
            model_name='client',
            name='time',
            field=models.TimeField(default='08:45:09'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='DOB',
            field=models.DateField(default='2020-06-20'),
        ),
        migrations.AlterField(
            model_name='paytm',
            name='bardate',
            field=models.DateField(default='2020-06-20'),
        ),
        migrations.AlterField(
            model_name='paytm',
            name='date',
            field=models.DateField(default='2020-06-20'),
        ),
        migrations.AlterField(
            model_name='paytm',
            name='time',
            field=models.TimeField(default='08:45:09'),
        ),
    ]
