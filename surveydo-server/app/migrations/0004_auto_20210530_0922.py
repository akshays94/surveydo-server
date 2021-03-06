# Generated by Django 3.1.7 on 2021-05-30 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_survey_surveyquestion_surveyresponse_surveyresponseanswer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveyquestion',
            name='configuration',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='surveyresponseanswer',
            name='answer',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
