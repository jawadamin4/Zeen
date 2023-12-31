from datetime import date

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Program(models.Model):
    PROGRAM_CHOICES = [
        ('months', 'months'),
        ('semesters', 'semesters'),
    ]
    name = models.CharField(max_length=255)
    program_type = models.CharField(max_length=50, choices=PROGRAM_CHOICES)
    duration_in_months = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Donor(models.Model):
    donor_name = models.OneToOneField(User, on_delete=models.CASCADE)
    donor_cnic = models.CharField(max_length=13)
    donor_contact = models.IntegerField()
    donor_email = models.EmailField()
    donor_country = models.CharField(max_length=30)

    # Add any additional fields for the donor profile

    def __str__(self):
        return self.donor_name.username


class Verification(models.Model):
    application = models.OneToOneField('Application', on_delete=models.CASCADE, unique=True)
    verifier_name = models.CharField(max_length=255)
    verifier_email = models.EmailField()
    verifier_contact = models.CharField(max_length=15)
    verification_date = models.DateField(null=True, blank=True)
    verification_method = models.TextField(null=True, blank=True)
    recommendation = models.TextField(null=True, blank=True)

    move_for_interview = models.CharField(max_length=15, choices=[('-', '-'), ('yes', 'yes'), ('no', 'no')],
                                          default='-')
    status = models.CharField(max_length=30,
                              choices=[('Pending', 'Pending'), ('Accepted by verifier', 'Accepted by verifier'),
                                       ('Rejected by verifier', 'Rejected by verifier')],
                              default='Pending')

    def __str__(self):
        return f"Verification for {self.application.name} - {self.application.status}"

    class Meta:
        verbose_name = 'Verification'
        verbose_name_plural = '2:Verifications'


class Degree(models.Model):
    STATUS=[
        ('In Progress','In Progress'),
        ('Completed', 'Completed')
    ]
    application = models.ForeignKey('Application', on_delete=models.CASCADE)
    degree_name = models.CharField(max_length=255)
    status = models.CharField(max_length=100,choices=STATUS)
    institute_name = models.CharField(max_length=255)
    grade = models.CharField(max_length=10)  # You can change this field type based on your needs

    def __str__(self):
        return f"{self.degree_name} - {self.application.name}"

    class Meta:
        verbose_name_plural = 'Degrees'


class Application(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    LEVEL_CHOICES = [
        ('Primary School', 'Primary School'),
        ('Secondary School', 'Secondary School'),
        ('Intermediate', 'Intermediate'),
        ('O levels ', 'O levels '),
        ('A levels ', 'A levels '),
        ('Metrics', 'Metrics'),
        ('FSC', 'FSC'),
        ('Bachelors Degree', 'Bachelors Degree'),
        ('Masters', 'Masters'),
        ('Diploma / Certificate', 'Diploma / Certificate'),
        ('Other', 'Other'),
        # Add other levels as needed
    ]
    EducationProgram_Choices = [
        ('Primary School', 'Primary School'),
        ('Secondary School', 'Secondary School'),
        ('Intermediate', 'Intermediate'),
        ('O levels ', 'O levels '),
        ('A levels ', 'A levels '),
        ('Metrics', 'Metrics'),
        ('FSC', 'FSC'),
        ('Bachelors Degree', 'Bachelors Degree'),
        ('Masters', 'Masters'),
        ('Diploma / Certificate', 'Diploma / Certificate'),
        ('Other', 'Other'),

    ]

    name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    age = models.PositiveIntegerField(default=1)
    country = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=15)
    cnic_or_b_form = models.CharField(max_length=13)
    email = models.EmailField()
    village = models.CharField(max_length=255)
    address = models.TextField()
    current_level_of_education = models.CharField(max_length=255, choices=LEVEL_CHOICES)
    program_interested_in = models.ForeignKey(Program, on_delete=models.CASCADE, blank=True, null=True)
    institution_interested_in = models.CharField(max_length=255)
    admission_fee_of_the_program = models.DecimalField(max_digits=10, decimal_places=2)
    total_fee_of_the_program = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Total Fee Of Program '
                                                                                                 '(per month)')
    account_expenses = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Account Expenses   '
                                                                                         '(per month)')
    living_expenses = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Account Expenses   '
                                                                                        '(per month)')
    food_and_necessities_expenses = models.DecimalField(max_digits=10, decimal_places=2,
                                                        verbose_name='Food & Necessities expenses (per month)')
    transport_amount = models.DecimalField(max_digits=10, decimal_places=2)
    other_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_members_of_household = models.IntegerField()
    members_earning = models.IntegerField()
    income_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    expense_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    description_of_household = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    personal_statement = models.TextField()
    account_title = models.CharField(max_length=255, null=True, blank=True)
    bank_account_number = models.CharField(max_length=20, null=True, blank=True)
    bank_name = models.CharField(max_length=255, null=True, blank=True)
    degrees = models.ManyToManyField(Degree, related_name='degrees', blank=True)
    degree_document = models.FileField(upload_to='documents/', null=True, blank=True)
    transcript_document = models.FileField(upload_to='documents/', null=True, blank=True)
    income_statement_document = models.FileField(upload_to='documents/', null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    status = models.CharField(max_length=20,
                              choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')],
                              default='Pending')

    verification_required = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.calculate_total_amount()
        self.calculate_age()
        # Validate age
        self.clean()
        super().save(*args, **kwargs)

    def calculate_age(self):
        today = date.today()
        birth_date = self.date_of_birth
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        self.age = age

    def calculate_total_amount(self):
        # Your calculation logic here
        self.total_amount = self.admission_fee_of_the_program + self.total_fee_of_the_program + self.account_expenses + self.living_expenses + self.transport_amount + self.food_and_necessities_expenses + self.other_amount

    def clean(self):
        if self.age <= 0:
            raise ValidationError("Age must be a positive integer.")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '1:Application'


class Interview(models.Model):
    application = models.OneToOneField('Application', on_delete=models.CASCADE)
    interviewer_name = models.CharField(max_length=255)
    interview_date = models.DateField(null=True, blank=True)
    question_1 = models.TextField(verbose_name='Ask about student profile')
    question_2 = models.TextField(verbose_name='Ask student\'s family background and analyze financial circumstances')
    question_3 = models.TextField(
        verbose_name='Ask about student\'s career plans and future aspirations regarding studies or career')
    question_4 = models.TextField(verbose_name='How was education being financed till now?')
    question_5 = models.TextField(
        verbose_name='How much financial support is required and what amount will be student contribution')
    question_6 = models.TextField(verbose_name='For how long will the financial support be required?')
    question_7 = models.TextField(
        verbose_name='Ask student if he/she was planning to manage his/her studies, especially if they have already '
                     'started a program?')
    question_8 = models.TextField(verbose_name='Why does the student feel he/she deserves this sponsorship?')
    question_9 = models.TextField(
        verbose_name='What are the student\'s plans for self-sufficiency or increase in contribution in the future?')
    question_10 = models.TextField(
        verbose_name='Summary of responses to any other question that the interview raised during the interview')
    question_11 = models.TextField(
        verbose_name='Assess all the above with the personal statement included in the application form and give '
                     'recommendations for the case')
    interviewer_recommendation = models.TextField()
    Accepted = models.CharField(max_length=15, choices=[('-', '-'), ('yes', 'yes'), ('no', 'no')],
                                default='-')
    status = models.CharField(max_length=30,
                              choices=[('Pending', 'Pending'), ('Accepted by interviewer', 'Accepted by interviewer'),
                                       ('Rejected by interviewer', 'Rejected by interviewer')],
                              default='Pending')

    def __str__(self):
        return f"Interview for {self.application.name}"

    class Meta:
        verbose_name = 'Interview'
        verbose_name_plural = '3:Interviews'


class SelectDonor(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    Donor = models.ForeignKey(Donor, on_delete=models.CASCADE, null=True, blank=True)
    selection_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '5:Select_Donor'


class Student(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    username = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=False, unique=True)
    student_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    age = models.PositiveIntegerField()
    country = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=15)
    email = models.EmailField()
    village = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return f"{self.username.username}"

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"


class ProjectionSheet(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.PositiveIntegerField()
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=0)
    other_fee = models.DecimalField(max_digits=10, decimal_places=0)
    total_cost = models.DecimalField(max_digits=10, decimal_places=0)
    sponsor_name = models.CharField(max_length=255)
    sponsorship_commitment = models.DecimalField(max_digits=5, decimal_places=0)
    fee_due_date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], default='Unpaid')
    payment_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Projection Sheet - {self.student.username.username} - Semester {self.semester}"
