# Generated by Django 5.0.6 on 2024-06-28 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApi', '0052_remove_person_tabletype_remove_table_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='table',
            name='tableno',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]