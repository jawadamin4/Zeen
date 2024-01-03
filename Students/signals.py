# students/signals.py
from datetime import timedelta

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Application, Verification, Interview, SelectDonor, Student, ProjectionSheet, Program, Donor, \
    SelectMentor, Mentor
from django.utils.crypto import get_random_string
from django.conf import settings


# Define a signal for projection sheet creation


@receiver(post_save, sender=Application)
def handle_application_save(sender, instance, created, **kwargs):
    """
    Signal handler to perform actions when an Application is saved.
    """
    if instance.status == 'Accepted' and instance.verification_required:
        # Check if a Verification instance already exists for this Application
        existing_verification = Verification.objects.filter(application=instance).first()

        if not existing_verification:
            Verification.objects.create(application=instance)


@receiver(post_save, sender=Verification)
def create_interview(sender, instance, created, **kwargs):
    """
    Signal handler to create an Interview instance when move_for_interview is set to yes.
    """
    if not created and instance.move_for_interview == 'yes':
        # Check if an Interview instance already exists for this Verification
        existing_interview = Interview.objects.filter(application=instance.application).first()

        if not existing_interview:
            Interview.objects.create(application=instance.application)
            Verification.objects.filter(pk=instance.pk).update(status='Accepted by verifier')
    elif not created and instance.move_for_interview == 'no' and instance.status != 'Rejected by verifier':
        Verification.objects.filter(pk=instance.pk).update(status='Rejected by verifier')
    elif not created and instance.move_for_interview == '-':
        Verification.objects.filter(pk=instance.pk).update(status='pending')


@receiver(post_save, sender=Interview)
def interview_status_change(sender, instance, **kwargs):
    """
    Signal handler to perform actions when the status of an Interview changes.
    """
    if instance.Accepted == 'yes':
        # Check if a Student account already exists for the student
        existing_student = Student.objects.filter(user__username=instance.application.cnic_or_b_form).first()

        if not existing_student:
            random_password = get_random_string(length=12)
            print(random_password)
            # Create a Student account for the student with the application information
            student_user = User.objects.create_user(
                username=instance.application.cnic_or_b_form,
                email=instance.application.email,
                password=random_password,
                first_name=instance.application.name,
                last_name=instance.application.last_name,
            )

            subject = 'Welcome to ZEEN STUDENT SCHOLARSHIP PROJECT!'
            message = f'Thank you for registering with ZEEN STUDENT SCHOLARSHIP PROJECT!\n\n'f'Your username: "{instance.application.cnic_or_b_form}"\n'f'Your password: {random_password}\n\n' f'Please log in using your username & password.'

            from_email = settings.EMAIL_HOST_USER
            recipient_list = [instance.application.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            student = Student.objects.create(
                user=student_user,
                student_name=instance.application.name,
                application=instance.application,
                father_name=instance.application.father_name,
                last_name=instance.application.last_name,
                gender=instance.application.gender,
                date_of_birth=instance.application.date_of_birth,
                age=instance.application.age,
                country=instance.application.country,
                province=instance.application.province,
                city=instance.application.city,
                mobile_no=instance.application.mobile_no,
                email=instance.application.email,
                village=instance.application.village,
                address=instance.application.address,
            )
            SelectMentor.objects.create(student=student)
            # program_durations_in_months = {
            #     'Primary School': 60,
            #     'Secondary School': 36,
            #     'Intermediate': 24,
            #     'O levels': 24,
            #     'A levels': 24,
            #     'Metrics': 24,
            #     'FSC': 24,
            #     'Bachelors Degree': 48,
            #     'Masters': 24,
            #     'Diploma / Certificate': 12,  # Varies, set as an example
            #     'Other': 12,  # Varies, set as an example
            # }

            # Get the program information
            program_info = Program.objects.filter(name=instance.application.program_interested_in).first()

            if program_info:
                # Calculate the duration of the program in semesters or months
                if program_info.program_type == "semesters":
                    duration_in_units = program_info.duration_in_months // 6
                else:
                    duration_in_units = program_info.duration_in_months

                # Get the student associated with the interview
                student = Student.objects.get(user__username=instance.application.cnic_or_b_form)

                # Calculate the start date for projections
                start_date = instance.interview_date

                # Automatically generate projection sheets for multiple semesters or months
                for unit in range(1, duration_in_units + 1):
                    # Calculate the fee due date based on the interview date
                    fee_due_date = start_date + timedelta(
                        days=180 * (unit - 1)) if program_info.program_type == "semesters" \
                        else start_date + timedelta(days=30 * (unit - 1))

                    # Adjust the values based on your actual fee calculation logic
                    tuition_fee = 0  # Set the actual tuition fee for each unit
                    other_fee = 0  # Set the actual other fee for each unit
                    total_cost = 0  # Update with the actual calculation for each unit

                    # Create a ProjectionSheet instance for the unit
                    projection_sheet = ProjectionSheet(
                        student=student,
                        semester=unit,
                        tuition_fee=tuition_fee,
                        other_fee=other_fee,
                        total_cost=total_cost,
                        sponsor_name="",  # Update with dynamic sponsor name
                        sponsorship_commitment=100,  # Update with the actual commitment percentage
                        fee_due_date=fee_due_date,
                        status='Unpaid',
                    )
                    projection_sheet.save()

        # Check if a SelectDonor instance already exists for the application
        if not SelectDonor.objects.filter(application=instance.application).exists():
            # Create a SelectDonor instance for the accepted interview
            SelectDonor.objects.create(application=instance.application)

            # Create a SelectDonor instance for the accepted interview
        Interview.objects.filter(pk=instance.pk).update(status='Accepted by interviewer')
    elif instance.Accepted == 'no' and instance.status != 'Rejected by interviewer':
        Interview.objects.filter(pk=instance.pk).update(status='Rejected by interviewer')
    elif instance.Accepted == '-':
        Interview.objects.filter(pk=instance.pk).update(status='pending')
        # Save the updated instance


@receiver(post_save, sender=Donor)
def create_user_and_link(sender, instance, created, **kwargs):
    if created and not instance.donor_username:
        # Create a new User instance with a random password
        password = User.objects.make_random_password()
        user = User.objects.create(username=instance.donor_cnic,email=instance.donor_email,first_name=instance.donor_name,
                                   password=make_password(password))
        instance.donor_username = user
        instance.save()
        subject = 'Welcome to ZEEN STUDENT SCHOLARSHIP PROJECT!'
        message = f'You are selected as Donor in  ZEEN STUDENT SCHOLARSHIP PROJECT!\n\n'f'Your username: "{instance.donor_cnic}"\n'f'Your password: {password}\n\n' f'Please log in using your username & password. '

        from_email = settings.EMAIL_HOST_USER
        recipient_list = [instance.donor_email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        print(f"Password for {user.username}: {password}")


@receiver(post_save, sender=Mentor)
def create_user_and_link(sender, instance, created, **kwargs):
    if created and not instance.mentor_username:
        # Create a new User instance with a random password
        password = User.objects.make_random_password()
        user = User.objects.create(username=instance.mentor_cnic,email=instance.mentor_email,first_name=instance.mentor_name,
                                   password=make_password(password))
        instance.mentor_username = user
        instance.save()
        subject = 'Welcome to ZEEN STUDENT SCHOLARSHIP PROJECT!'
        message = f'You are selected as Mentor in  ZEEN STUDENT SCHOLARSHIP PROJECT!\n\n'f'Your username: "{instance.mentor_cnic}"\n'f'Your password: {password}\n\n' f'Please log in using your username & password. '

        from_email = settings.EMAIL_HOST_USER
        recipient_list = [instance.mentor_email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        print(f"Password for {user.username}: {password}")