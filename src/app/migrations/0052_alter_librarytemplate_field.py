# Generated by Django 5.1.4 on 2025-03-06 17:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0051_rename_all_library_templates_blocktemplate_library_templates_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='librarytemplate',
            name='field',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='library_templates', to='app.field'),
        ),
    ]
