# Generated by Django 5.0 on 2023-12-21 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Students', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interview',
            name='interview_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]