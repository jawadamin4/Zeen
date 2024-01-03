# Generated by Django 4.2.6 on 2024-01-03 08:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Students', '0024_donor_donor_username_alter_degree_status_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mentor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mentor_name', models.CharField(max_length=30)),
                ('mentor_cnic', models.CharField(max_length=13)),
                ('mentor_contact', models.IntegerField()),
                ('mentor_email', models.EmailField(max_length=254)),
                ('mentor_Expertise', models.CharField(max_length=30)),
                ('mentor_country', models.CharField(max_length=30)),
                ('mentor_username', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterModelOptions(
            name='selectdonor',
            options={'verbose_name_plural': '4:Select_Donor'},
        ),
        migrations.RenameField(
            model_name='selectdonor',
            old_name='Donor',
            new_name='donor',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='username',
            new_name='user',
        ),
        migrations.AddField(
            model_name='student',
            name='application',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Students.application'),
        ),
        migrations.AlterField(
            model_name='selectdonor',
            name='selection_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name='SelectMentor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selection_date', models.DateTimeField(auto_now=True)),
                ('mentor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Students.mentor')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Students.student')),
            ],
            options={
                'verbose_name_plural': '6:Select_Mentor',
            },
        ),
    ]