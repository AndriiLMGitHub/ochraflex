# Generated by Django 5.1.4 on 2025-01-07 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_delete_selectoption'),
    ]

    operations = [
        migrations.AlterField(
            model_name='field',
            name='field_type',
            field=models.CharField(choices=[('text', 'Text'), ('textarea', 'Textarea'), ('number', 'Number'), ('select', 'Select'), ('checkbox', 'Checkbox'), ('radio', 'Radio'), ('date', 'Date'), ('boolean', 'Boolean')], max_length=50),
        ),
    ]
