# Generated by Django 5.0 on 2023-12-21 11:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('father_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10)),
                ('date_of_birth', models.DateField()),
                ('age', models.IntegerField()),
                ('country', models.CharField(max_length=255)),
                ('province', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('mobile_no', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('village', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('level_of_education', models.CharField(choices=[('High School', 'High School'), ('Undergraduate', 'Undergraduate'), ('Graduate', 'Graduate')], max_length=255)),
                ('program_interested_in', models.CharField(max_length=255)),
                ('institution_name', models.CharField(max_length=255)),
                ('total_cost_of_program', models.DecimalField(decimal_places=2, max_digits=10)),
                ('accommodation_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('living_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transport_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('other_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_members_of_household', models.IntegerField()),
                ('members_earning', models.IntegerField()),
                ('income_per_month', models.DecimalField(decimal_places=2, max_digits=10)),
                ('expense_per_month', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('personal_statement', models.TextField()),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Pending', max_length=20)),
                ('verification_required', models.BooleanField(default=False)),
                ('verification_submitted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Degree',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree_name', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=100)),
                ('institute_name', models.CharField(max_length=255)),
                ('grade', models.CharField(max_length=10)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Students.application')),
            ],
        ),
        migrations.AddField(
            model_name='application',
            name='degrees',
            field=models.ManyToManyField(blank=True, related_name='degrees', to='Students.degree'),
        ),
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interviewer_name', models.CharField(max_length=255)),
                ('interview_date', models.DateField(blank=True)),
                ('question_1', models.TextField()),
                ('question_2', models.TextField()),
                ('question_3', models.TextField()),
                ('question_4', models.TextField()),
                ('question_5', models.TextField()),
                ('question_6', models.TextField()),
                ('question_7', models.TextField()),
                ('question_8', models.TextField()),
                ('question_9', models.TextField()),
                ('question_10', models.TextField()),
                ('question_11', models.TextField()),
                ('summary_responses', models.TextField()),
                ('recommendations', models.TextField()),
                ('interviewer_recommendation', models.TextField()),
                ('application', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Students.application')),
            ],
        ),
        migrations.CreateModel(
            name='Verification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verifier_name', models.CharField(max_length=255)),
                ('verifier_email', models.EmailField(max_length=254)),
                ('verifier_contact', models.CharField(max_length=15)),
                ('verification_date', models.DateField(blank=True, null=True)),
                ('cnic_or_b_form', models.CharField(blank=True, max_length=255, null=True)),
                ('verification_method', models.TextField(blank=True, null=True)),
                ('recommendation', models.TextField(blank=True, null=True)),
                ('move_for_interview', models.BooleanField(default=False)),
                ('application', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Students.application')),
            ],
            options={
                'verbose_name': 'Verification',
                'verbose_name_plural': 'Verifications',
            },
        ),
    ]
