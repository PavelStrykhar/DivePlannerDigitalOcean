# Generated by Django 3.2.9 on 2022-05-02 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0022_auto_20220501_0019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='is_attending',
        ),
    ]