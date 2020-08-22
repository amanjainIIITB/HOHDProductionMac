# Generated by Django 3.0.5 on 2020-08-08 12:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0028_auto_20200801_0659'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('contact_number', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1000000000), django.core.validators.MaxValueValidator(9999999999)])),
                ('date', models.DateField(default='2020-08-08')),
                ('start_time', models.CharField(max_length=50, null=True)),
                ('end_time', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='employee',
            name='DOB',
            field=models.DateField(default='2020-08-08'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='date_of_joining',
            field=models.DateField(default='2020-08-08'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateField(default='2020-08-08'),
        ),
    ]