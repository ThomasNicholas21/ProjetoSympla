# Generated by Django 5.2.4 on 2025-07-23 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_event_delete_events'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='sympla_id',
            field=models.CharField(max_length=128),
        ),
    ]
