# Generated by Django 5.1.4 on 2025-01-21 18:36

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_field_uuid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='field',
            name='uuid',
        ),
        migrations.AddField(
            model_name='blocktemplate',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
