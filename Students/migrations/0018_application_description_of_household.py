# Generated by Django 5.0 on 2023-12-28 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Students', '0017_remove_interview_recommendations_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='description_of_household',
            field=models.TextField(default='xyz'),
            preserve_default=False,
        ),
    ]