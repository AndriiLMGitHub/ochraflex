# Generated by Django 5.1.4 on 2025-03-04 18:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0050_rename_library_templates_blocktemplate_all_library_templates_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blocktemplate',
            old_name='all_library_templates',
            new_name='library_templates',
        ),
        migrations.RemoveField(
            model_name='blocktemplate',
            name='all_combined_blocks',
        ),
        migrations.RemoveField(
            model_name='blocktemplate',
            name='all_description_fields',
        ),
        migrations.RemoveField(
            model_name='blocktemplate',
            name='all_fields',
        ),
    ]
