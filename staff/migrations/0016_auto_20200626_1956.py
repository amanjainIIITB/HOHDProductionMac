# Generated by Django 3.0.5 on 2020-06-26 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0015_auto_20200621_0823'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopregistration',
            name='owner_list',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='DOB',
            field=models.DateField(default='2020-06-26'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='date_of_joining',
            field=models.DateField(default='2020-06-26'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateField(default='2020-06-26'),
        ),
    ]