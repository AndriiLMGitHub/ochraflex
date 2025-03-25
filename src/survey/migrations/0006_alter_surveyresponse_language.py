# Generated by Django 5.1.4 on 2025-03-25 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0005_surveyresponse_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveyresponse',
            name='language',
            field=models.CharField(blank=True, choices=[('cs', 'Czech Republic'), ('de', 'Germany')], default='cs', max_length=128, null=True),
        ),
    ]
