# students/signals.py
from datetime import timedelta

import pandas as pd
from io import BytesIO
from django.core.files import File
import os
import openpyxl

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Application, Verification, Interview, SelectDonor, Student, ProjectionSheet, Program
from django.utils.crypto import get_random_string
from django.conf import settings
from django.dispatch import Signal

# Define a signal for projection sheet creation
# projection_sheet_created = Signal()


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
        existing_student = Student.objects.filter(username__username=instance.application.cnic_or_b_form).first()

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
                username=student_user,
                student_name=instance.application.name,
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
                if program_info.program_type == "months":
                    # Automatically generate projection sheets for multiple months
                    for month in range(1, program_info.duration_in_months + 1):
                        # Calculate the fee due date based on the interview date
                        fee_due_date = instance.interview_date + timedelta(days=30 * month)  # Adjust as needed

                        projection_sheet = ProjectionSheet(
                            student=student,
                            semester=month,  # You can set semester to None for months
                            tuition_fee=0,  # Set the actual tuition fee for each month
                            other_fee=0,  # Set the actual other fee for each month
                            total_cost=0,  # Update with the actual calculation for each month
                            sponsor_name="",  # Update with dynamic sponsor name
                            sponsorship_commitment=100,  # Update with the actual commitment percentage
                            fee_due_date=fee_due_date,
                            status='Unpaid',
                        )
                        projection_sheet.save()

                elif program_info.program_type == "semesters":
                    # Automatically generate projection sheets for multiple semesters
                    for semester in range(1, program_info.duration_in_months // 6 + 1):
                        # Calculate the fee due date based on the interview date
                        fee_due_date = instance.interview_date + timedelta(days=180 * semester)  # Adjust as needed
                        type = program_info.program_type
                        projection_sheet = ProjectionSheet(
                            student=student,
                            semester=semester,
                            tuition_fee=0,  # Set the actual tuition fee for each semester
                            other_fee=0,  # Set the actual other fee for each semester
                            total_cost=0,  # Update with the actual calculation for each semester
                            sponsor_name=type,  # Update with dynamic sponsor name
                            sponsorship_commitment=0,  # Update with the actual commitment percentage
                            fee_due_date=fee_due_date,
                            status='Unpaid',
                        )
                        projection_sheet.save()


        # Check if a SelectDonor instance already exists for the application
        if not SelectDonor.objects.filter(application=instance.application).exists():
            # Create a SelectDonor instance for the accepted interview
            SelectDonor.objects.create(application=instance.application)
        Interview.objects.filter(pk=instance.pk).update(status='Accepted by interviewer')
    elif instance.Accepted == 'no' and instance.status != 'Rejected by interviewer':
        Interview.objects.filter(pk=instance.pk).update(status='Rejected by interviewer')
    elif instance.Accepted == '-':
        Interview.objects.filter(pk=instance.pk).update(status='pending')
        # Save the updated instance


# @receiver(post_save, sender=Interview)
# def create_forecast_entry(sender, instance, created, **kwargs):
#     """
#     Signal handler to create a ForecastEntry instance based on Interview recommendations.
#     """
#     if not created and instance.Accepted == 'yes':
#         # Check if a ForecastEntry instance already exists for this Application
#         existing_forecast_entry = ForecastEntry.objects.filter(application=instance.application).first()
#
#         if not existing_forecast_entry:
#             # Calculate fees based on interview recommendations and scholarship percentage
#             semester_fee, tuition_fee, other_fee, total_cost, scholarship_percentage = calculate_fees_based_on_interview(
#                 instance)
#
#             ForecastEntry.objects.create(
#                 application=instance.application,
#                 semester_fee=semester_fee,
#                 tuition_fee=tuition_fee,
#                 other_fee=other_fee,
#                 total_cost=total_cost,
#                 sponsor_name=instance.application.name,  # Assuming the student's name as the sponsor
#                 sponsorship_confirmation=True,  # You can adjust this based on your needs
#                 fee_due_date=instance.interview_date,  # You might want to adjust this based on your logic
#             )



# # Constants
# SEMESTER_FEE_PERCENTAGE = 0.5
#
# TUITION_FEE_PERCENTAGE = 0.3
# OTHER_FEE_PERCENTAGE = 0.2


# ...

# def calculate_fees_based_on_interview(interview_instance):
#     """
#     Calculate fees based on interview recommendations and scholarship percentage.
#     Replace this with your actual logic.
#     """
#     try:
#         # Sample logic (replace with your actual calculation)
#         # Replace with your calculation
#
#         # Extract scholarship information from the interview recommendation
#         scholarship_percentage = extract_scholarship_percentage(interview_instance.interviewer_recommendation)
#         print(scholarship_percentage)
#         # Calculate fees based on scholarship percentage
#         # Convert total_expense to float
#         total_expense = float(interview_instance.application.total_amount)
#         print(total_expense)
#         total_cost_before_scholarship = total_expense * (1 - scholarship_percentage)
#         semester_fee = total_cost_before_scholarship * SEMESTER_FEE_PERCENTAGE
#         tuition_fee = total_cost_before_scholarship * TUITION_FEE_PERCENTAGE
#         other_fee = total_cost_before_scholarship * OTHER_FEE_PERCENTAGE
#         total_cost = semester_fee + tuition_fee + other_fee
#         print(total_cost_before_scholarship, semester_fee, tuition_fee, other_fee, total_cost)
#
#         return semester_fee, tuition_fee, other_fee, total_cost, scholarship_percentage
#     except Exception as e:
#         # Handle exceptions (e.g., invalid scholarship information)
#         print(f"Error calculating fees: {e}")
#         return 0.0, 0.0, 0.0, 0.0, 0.0
#
#
# def extract_scholarship_percentage(recommendation_text):
#     """
#     Extract scholarship percentage from the interview recommendation.
#     Replace this with your actual extraction logic.
#     """
#     # Sample extraction logic (replace with your actual extraction)
#     # Assuming the recommendation text contains the scholarship percentage
#     # in the format "Scholarship: 50%"
#     scholarship_keyword = 'Scholarship:'
#     percentage_index = recommendation_text.find(scholarship_keyword)
#
#     if percentage_index != -1:
#         percentage_str = recommendation_text[percentage_index + len(scholarship_keyword):].strip('%').strip()
#         try:
#             scholarship_percentage = float(percentage_str) / 100
#             print(scholarship_percentage)
#             return scholarship_percentage
#         except ValueError:
#             pass
#
#     # Default to no scholarship if not found or invalid
#     return 0.0


#
# @receiver(post_save, sender=Interview)
# def create_projection_sheet(sender, instance, created, **kwargs):
#     """
#     Signal handler to create a projection sheet based on Interview recommendations.
#     """
#     if not created and instance.Accepted == 'yes':
#         try:
#             # Calculate fees based on interview recommendations and scholarship percentage
#             semester_fee, tuition_fee, other_fee, total_cost, scholarship_percentage = calculate_fees_based_on_interview(
#                 instance)
#
#             # Create a DataFrame for the projection sheet
#             data = {
#                 "Semester": ["Replace with Semester"],  # Update with the actual semester
#                 "Tuition Fee (PKR)": [tuition_fee],
#                 "Other Fee (PKR)": [other_fee],
#                 "Total Cost (PKR)": [total_cost],
#                 "Sponsor Name": [instance.application.name],  # Assuming the student's name as the sponsor
#                 "Sponsorship Commitment (%)": [scholarship_percentage],  # You can adjust this based on your needs
#                 "Fee Due Date": [instance.interview_date],  # You might want to adjust this based on your logic
#                 "Status (Paid/Unpaid)": ["Pending"],
#                 "Payment Date": [None],
#             }
#
#             df = pd.DataFrame(data)
#
#             # Specify the 'projections' folder within STATIC_ROOT
#             projections_folder = os.path.join(settings.STATIC_ROOT, 'projections')
#
#             # Create the 'projections' folder if it doesn't exist
#             os.makedirs(projections_folder, exist_ok=True)
#
#             # Define the file path within the 'projections' folder
#             filename = f"{instance.application.name.replace(' ', '_')}_projection_sheet.xlsx"
#             file_path = os.path.join(projections_folder, filename)
#
#             # Convert DataFrame to Excel
#             df.to_excel(file_path, index=False, sheet_name="Projection Sheet")
#
#             # Signal that the file has been created
#             projection_sheet_created.send(sender=Interview, instance=instance, filename=filename)
#
#         except Exception as e:
#             # Handle exceptions (e.g., invalid scholarship information)
#             print(f"Error creating projection sheet: {e}")

