# Generated by Django 3.2.9 on 2022-04-22 10:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20220421_2156'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='time_create',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='time_update',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
