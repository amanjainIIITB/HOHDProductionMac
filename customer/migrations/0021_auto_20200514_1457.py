# Generated by Django 3.0.5 on 2020-05-14 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0020_auto_20200514_1448'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='shopID',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='bharatpe',
            name='time',
            field=models.TimeField(default='14:57:36'),
        ),
        migrations.AlterField(
            model_name='client',
            name='time',
            field=models.TimeField(default='14:57:36'),
        ),
        migrations.AlterField(
            model_name='paytm',
            name='time',
            field=models.TimeField(default='14:57:36'),
        ),
    ]
