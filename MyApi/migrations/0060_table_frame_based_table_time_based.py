# Generated by Django 5.0.6 on 2024-07-01 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApi', '0059_alter_table_played_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='frame_based',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='table',
            name='time_based',
            field=models.BooleanField(default=False),
        ),
    ]