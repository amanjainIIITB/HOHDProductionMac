# Generated by Django 3.0.5 on 2020-11-15 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0005_auto_20201011_1747'),
    ]

    operations = [
        migrations.CreateModel(
            name='Access',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regID', models.CharField(max_length=10, null=True)),
                ('shopID', models.CharField(max_length=10, null=True)),
                ('isowner', models.BooleanField(default=False)),
                ('page_list', models.TextField(blank='', default='', null=True)),
            ],
        ),
    ]
