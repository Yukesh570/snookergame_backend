# Generated by Django 5.0.4 on 2024-06-17 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApi', '0020_table_ac'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='button',
            field=models.BooleanField(default=False),
        ),
    ]
