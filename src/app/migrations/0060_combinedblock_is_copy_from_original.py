# Generated by Django 5.1.4 on 2025-04-07 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0059_combinedblock_is_from_library_template'),
    ]

    operations = [
        migrations.AddField(
            model_name='combinedblock',
            name='is_copy_from_original',
            field=models.BooleanField(default=False),
        ),
    ]
