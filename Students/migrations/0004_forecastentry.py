# Generated by Django 5.0 on 2023-12-23 09:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Students', '0003_alter_interview_question_1_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForecastEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester_fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tuition_fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('other_fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sponsor_name', models.CharField(max_length=255)),
                ('sponsorship_confirmation', models.CharField(max_length=255)),
                ('fee_due_date', models.DateField()),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending', max_length=20)),
                ('payment_date', models.DateField(blank=True, null=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Students.application')),
            ],
        ),
    ]
