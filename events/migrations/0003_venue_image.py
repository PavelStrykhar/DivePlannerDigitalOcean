# Generated by Django 3.2.9 on 2022-04-16 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_venue_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/events/%Y/%m/%d/'),
        ),
    ]
