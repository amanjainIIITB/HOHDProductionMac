# Generated by Django 3.0.5 on 2020-04-14 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default='2020-04-14')),
                ('purpose', models.CharField(max_length=100, null=True)),
                ('paymentmode', models.CharField(max_length=100, null=True)),
                ('comment', models.CharField(max_length=1000, null=True)),
                ('amount', models.IntegerField(default=0)),
            ],
        ),
    ]
