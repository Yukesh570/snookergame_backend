# Generated by Django 5.0.6 on 2024-06-26 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApi', '0048_rename_tabletype_id_person_tabletype'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='is_running',
        ),
        migrations.AddField(
            model_name='table',
            name='is_running',
            field=models.BooleanField(default=False),
        ),
    ]
