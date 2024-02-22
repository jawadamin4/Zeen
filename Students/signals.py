# students/signals.py
from datetime import timedelta

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Application, Verification, Interview, SelectDonor, Student, ProjectionSheet, Program, Donor, \
    SelectMentor, Mentor
from django.db.utils import IntegrityError
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
        # Check if a SelectMentor instance already exists for the student
        existing_mentor = SelectMentor.objects.filter(student=instance.application.student).first()
        if not existing_mentor:
            # Create a SelectMentor instance for the accepted interview
            SelectMentor.objects.create(student=instance.application.student)
        # program_info = Program.objects.filter(name=instance.application.program_interested_in).first()
        #
        # if program_info:
        #     # Calculate the duration of the program in semesters or months
        #     if program_info.program_type == "semesters":
        #         duration_in_units = program_info.duration_in_months // 6
        #     else:
        #         duration_in_units = program_info.duration_in_months
        #
        #     # Get the student associated with the interview
        #     # student = Student.objects.get(user__username=instance.application.cnic_or_b_form)
        #     #
        #     # Calculate the start date for projections
        #     start_date = instance.interview_date
        #
        #     # Automatically generate projection sheets for multiple semesters or months
        #     for unit in range(1, duration_in_units + 1):
        #         # Calculate the fee due date based on the interview date
        #         fee_due_date = start_date + timedelta(
        #             days=180 * (unit - 1)) if program_info.program_type == "semesters" \
        #             else start_date + timedelta(days=30 * (unit - 1))
        #
        #         # Adjust the values based on your actual fee calculation logic
        #         tuition_fee = 0  # Set the actual tuition fee for each unit
        #         other_fee = 0  # Set the actual other fee for each unit
        #         total_cost = 0  # Update with the actual calculation for each unit
        #
        #         # Create a ProjectionSheet instance for the unit
        #         projection_sheet = ProjectionSheet(
        #             student=instance.application.student,
        #             semester=unit,
        #             tuition_fee=tuition_fee,
        #             other_fee=other_fee,
        #             total_cost=total_cost,
        #             sponsor_name="",  # Update with dynamic sponsor name
        #             sponsorship_commitment=100,  # Update with the actual commitment percentage
        #             fee_due_date=fee_due_date,
        #             status='Unpaid',
        #         )
        #         projection_sheet.save()

        # Check if a SelectDonor instance already exists for the application
        if not SelectDonor.objects.filter(student=instance.application.student).exists():
            # Create a SelectDonor instance for the accepted interview
            SelectDonor.objects.create(student=instance.application.student)

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
        password = instance.donor_name + "123"
        user = User.objects.create(username=instance.donor_cnic, email=instance.donor_email,
                                   first_name=instance.donor_name,
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
        password = instance.mentor_name + "123"
        user = User.objects.create(username=instance.mentor_cnic, email=instance.mentor_email,
                                   first_name=instance.mentor_name,
                                   password=make_password(password))
        instance.mentor_username = user
        instance.save()
        subject = 'Welcome to ZEEN STUDENT SCHOLARSHIP PROJECT!'
        message = f'You are selected as Mentor in  ZEEN STUDENT SCHOLARSHIP PROJECT!\n\n'f'Your username: "{instance.mentor_cnic}"\n'f'Your password: {password}\n\n' f'Please log in using your username & password. '

        from_email = settings.EMAIL_HOST_USER
        recipient_list = [instance.mentor_email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        print(f"Password for {user.username}: {password}")
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
@receiver(post_save, sender=Student)
def create_user_and_link(sender, instance, created, **kwargs):
    if created and not instance.user:
        # Assuming `user` is the ForeignKey field linking Student to User
        # Create a new User instance with the student's email as the username
        password = instance.student_name + "123"  # Generate a random password
        try:
            user = User.objects.create(username=instance.student_name,
                                       password=make_password(password))
            instance.user = user
            instance.save()
        except IntegrityError as e:
            # If a UNIQUE constraint violation occurs on the username field
            # Delete the user instance and avoid saving the student instance
            if 'UNIQUE constraint failed: auth_user.username' in str(e):
                user.delete()
                print("Username already exists. Student creation aborted.")