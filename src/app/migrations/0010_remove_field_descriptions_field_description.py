# Generated by Django 5.1.4 on 2025-01-06 12:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_remove_descriptionfield_field_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='field',
            name='descriptions',
        ),
        migrations.AddField(
            model_name='field',
            name='description',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='app.descriptionfield'),
        ),
    ]
