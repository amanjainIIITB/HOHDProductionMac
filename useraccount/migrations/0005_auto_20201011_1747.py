# Generated by Django 3.0.5 on 2020-10-11 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0004_auto_20201011_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ownerregistration',
            name='shop_list',
            field=models.TextField(blank='', default='', null=True),
        ),
    ]
