# Generated by Django 4.2.6 on 2024-01-02 07:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Students', '0023_application_account_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='donor',
            name='donor_username',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='degree',
            name='status',
            field=models.CharField(choices=[('In Progress', 'In Progress'), ('Completed', 'Completed')], max_length=100),
        ),
        migrations.AlterField(
            model_name='donor',
            name='donor_name',
            field=models.CharField(max_length=30),
        ),
    ]