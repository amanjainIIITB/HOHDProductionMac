# Generated by Django 3.0.5 on 2020-05-01 07:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('useraccount', '0002_delete_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('mobile', models.CharField(max_length=10, null=True)),
            ],
        ),
    ]
