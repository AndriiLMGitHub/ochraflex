# Generated by Django 5.1.4 on 2025-03-24 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldresponse',
            name='input_method',
            field=models.CharField(blank=True, choices=[('paste', 'Paste'), ('keydown', 'Keydown')], max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='fieldresponse',
            name='input_time',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
