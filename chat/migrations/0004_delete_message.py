# Generated by Django 3.0.5 on 2020-06-16 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_auto_20200616_0946'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Message',
        ),
    ]
