# Generated by Django 5.1.4 on 2025-04-04 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0007_surveyresponsefavorite'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyresponse',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
