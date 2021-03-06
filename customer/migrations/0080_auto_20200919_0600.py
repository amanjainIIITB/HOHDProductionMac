# Generated by Django 3.0.5 on 2020-09-19 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0079_auto_20200906_1654'),
    ]

    operations = [
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default='2020-09-19')),
                ('time', models.TimeField(default='06:00:06')),
                ('shopID', models.CharField(max_length=10, null=True)),
                ('Name', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='clientvisit',
            name='date',
            field=models.DateField(default='2020-09-19'),
        ),
        migrations.AlterField(
            model_name='clientvisit',
            name='time',
            field=models.TimeField(default='06:00:06'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='last_visit',
            field=models.DateField(default='2020-09-19'),
        ),
    ]
