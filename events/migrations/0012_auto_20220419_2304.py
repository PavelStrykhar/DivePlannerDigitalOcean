# Generated by Django 3.2.9 on 2022-04-19 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_remove_participant_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='venue',
            name='long',
            field=models.FloatField(blank=True, null=True),
        ),
    ]