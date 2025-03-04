# Generated by Django 5.1.4 on 2025-01-05 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_field_field_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='field',
            name='field_type',
            field=models.CharField(choices=[('text', 'Text'), ('number', 'Number'), ('select', 'Select'), ('checkbox', 'Checkbox'), ('radio', 'Radio'), ('date', 'Date')], max_length=50),
        ),
        migrations.AlterField(
            model_name='field',
            name='name',
            field=models.CharField(max_length=1000),
        ),
    ]
