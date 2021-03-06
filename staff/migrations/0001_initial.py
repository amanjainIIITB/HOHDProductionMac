# Generated by Django 3.0.5 on 2020-09-06 12:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('contact_number', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1000000000), django.core.validators.MaxValueValidator(9999999999)])),
                ('date', models.DateField(default='2020-09-06')),
                ('start_time', models.TimeField(max_length=50, null=True)),
                ('end_time', models.TimeField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EmployeeID', models.CharField(max_length=10, null=True)),
                ('ShopID', models.CharField(max_length=10, null=True)),
                ('name', models.CharField(max_length=50, null=True)),
                ('contact_number', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1000000000), django.core.validators.MaxValueValidator(9999999999)])),
                ('sex', models.CharField(max_length=10, null=True)),
                ('date_of_joining', models.DateField(default='2020-09-06')),
                ('position', models.CharField(max_length=50, null=True)),
                ('DOB', models.DateField(null=True, blank=True)),
                ('temporary_address', models.TextField(max_length=1000, null=True)),
                ('permanent_address', models.TextField(max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ExpenseID', models.CharField(default='E1', max_length=10)),
                ('date', models.DateField(default='2020-09-06')),
                ('shopID', models.CharField(default='S1', max_length=10)),
                ('purpose', models.CharField(max_length=100, null=True)),
                ('paymentmode', models.CharField(max_length=100, null=True)),
                ('comment', models.CharField(max_length=1000, null=True)),
                ('amount', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ShopRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ShopID', models.CharField(max_length=10, null=True)),
                ('Desk_Contact_Number', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1000000000), django.core.validators.MaxValueValidator(9999999999)])),
                ('Shop_Name', models.CharField(max_length=50, null=True)),
                ('Shop_Address', models.TextField(max_length=1000, null=True)),
                ('owner_list', models.TextField(null=True)),
                ('email', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]
