# Generated by Django 3.0.5 on 2020-09-19 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0080_auto_20200919_0600'),
    ]

    operations = [
        migrations.AddField(
            model_name='services',
            name='visitID',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='clientvisit',
            name='time',
            field=models.TimeField(default='07:05:38'),
        ),
        migrations.AlterField(
            model_name='services',
            name='time',
            field=models.TimeField(default='07:05:38'),
        ),
    ]
