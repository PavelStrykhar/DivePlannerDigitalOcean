# Generated by Django 3.2.9 on 2022-04-28 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0019_event_short_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='short_description',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
