# Generated by Django 5.0.4 on 2024-06-17 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApi', '0022_table_inactive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='rate',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7, null=True),
        ),
    ]
