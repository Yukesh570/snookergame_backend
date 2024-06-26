# Generated by Django 5.0.4 on 2024-06-10 05:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApi', '0002_table_remove_address_address_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='address',
        ),
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.EmailField(max_length=200, null=True),
        ),
        migrations.RemoveField(
            model_name='person',
            name='phone',
        ),
        migrations.RenameField(
            model_name='person',
            old_name='first_name',
            new_name='Name',
        ),
        migrations.RemoveField(
            model_name='person',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='person',
            name='table_type',
        ),
        migrations.AddField(
            model_name='person',
            name='Phonenumber',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='table',
            name='person',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='MyApi.person'),
        ),
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.AddField(
            model_name='person',
            name='Address',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.DeleteModel(
            name='Email',
        ),
        migrations.DeleteModel(
            name='Phone',
        ),
    ]
