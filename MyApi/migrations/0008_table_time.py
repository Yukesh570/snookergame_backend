# Generated by Django 5.0.4 on 2024-06-10 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApi', '0007_alter_person_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='time',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
    ]
