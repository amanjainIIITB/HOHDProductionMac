# Generated by Django 3.0.5 on 2020-10-11 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0002_ownerregistration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ownerregistration',
            name='shop_list',
            field=models.TextField(blank=True, null=True),
        ),
    ]
