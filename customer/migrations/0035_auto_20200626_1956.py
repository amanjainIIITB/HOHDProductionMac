# Generated by Django 3.0.5 on 2020-06-26 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0034_auto_20200621_0823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bharatpe',
            name='bardate',
            field=models.DateField(default='2020-06-26'),
        ),
        migrations.AlterField(
            model_name='bharatpe',
            name='date',
            field=models.DateField(default='2020-06-26'),
        ),
        migrations.AlterField(
            model_name='bharatpe',
            name='time',
            field=models.TimeField(default='19:56:38'),
        ),
        migrations.AlterField(
            model_name='client',
            name='bardate',
            field=models.DateField(default='2020-06-26'),
        ),
        migrations.AlterField(
            model_name='client',
            name='date',
            field=models.DateField(default='2020-06-26'),
        ),
        migrations.AlterField(
            model_name='client',
            name='time',
            field=models.TimeField(default='19:56:38'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='DOB',
            field=models.DateField(default='2020-06-26'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='last_visit',
            field=models.DateField(default='2020-06-26'),
        ),
        migrations.AlterField(
            model_name='paytm',
            name='bardate',
            field=models.DateField(default='2020-06-26'),
        ),
        migrations.AlterField(
            model_name='paytm',
            name='date',
            field=models.DateField(default='2020-06-26'),
        ),
        migrations.AlterField(
            model_name='paytm',
            name='time',
            field=models.TimeField(default='19:56:38'),
        ),
    ]
