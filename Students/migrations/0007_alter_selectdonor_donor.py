# Generated by Django 5.0 on 2023-12-23 14:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Students', '0006_interview_status_alter_donor_donor_contact_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selectdonor',
            name='Donor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Students.donor'),
        ),
    ]