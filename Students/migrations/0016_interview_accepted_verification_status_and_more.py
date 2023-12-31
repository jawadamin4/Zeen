# Generated by Django 5.0 on 2023-12-28 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Students', '0015_rename_accommodation_amount_application_account_expenses_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='interview',
            name='Accepted',
            field=models.CharField(choices=[('-', '-'), ('yes', 'yes'), ('no', 'no')], default='no', max_length=15),
        ),
        migrations.AddField(
            model_name='verification',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Accepted by verifier', 'Accepted by verifier'), ('Rejected by verifier', 'Rejected by verifier')], default='Pending', max_length=30),
        ),
        migrations.AlterField(
            model_name='application',
            name='account_expenses',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Account Expenses   (per month)'),
        ),
        migrations.AlterField(
            model_name='application',
            name='age',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='application',
            name='cnic_or_b_form',
            field=models.CharField(default='123', max_length=13),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='application',
            name='food_and_necessities_expenses',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Food & Necessities expenses (per month)'),
        ),
        migrations.AlterField(
            model_name='application',
            name='living_expenses',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Account Expenses   (per month)'),
        ),
        migrations.AlterField(
            model_name='application',
            name='total_fee_of_the_program',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Total Fee Of Program (per month)'),
        ),
        migrations.AlterField(
            model_name='interview',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Accepted by interviewer', 'Accepted by interviewer'), ('Rejected by interviewer', 'Rejected by interviewer')], default='Pending', max_length=30),
        ),
        migrations.AlterField(
            model_name='verification',
            name='move_for_interview',
            field=models.CharField(choices=[('-', '-'), ('yes', 'yes'), ('no', 'no')], default='-', max_length=15),
        ),
    ]
