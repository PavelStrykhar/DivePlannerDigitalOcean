# Generated by Django 3.2.9 on 2022-04-26 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_rename_participant_event_participants'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='participants', to='events.Participant'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Participants', to='events.event'),
        ),
    ]