# zeen_app/serializers.py

from rest_framework import serializers
from .models import Application, Degree, Student, Program, ProjectionSheet, Results, Documents, BankDetails, \
    Verification, Interview, SelectDonor, Donor, SelectMentor, Mentor
from rest_framework.views import APIView


class ProgramSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    program_type = serializers.CharField(max_length=20)
    duration_in_months = serializers.IntegerField()

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Program.objects.create(**validated_data)


class DegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Degree
        fields = ['id', 'application', 'degree_name', 'status', 'institute_name', 'grade']


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Results
        fields = '__all__'


# --------------------------------------------Programs Serializer--------------------------------------
class ProgramSerializers(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'


class OtherDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = '__all__'


class ApplicationSerializer(serializers.ModelSerializer):
    program_interested_in = ProgramSerializers()
    degree = DegreeSerializer(many=True)

    # student = StudentSerializer(read_only=True)

    class Meta:
        model = Application
        fields = '__all__'

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['degrees'] = DegreeSerializer(instance.degrees.all(), many=True).data
    #     return representation


class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['name', 'father_name', 'last_name', 'gender', 'date_of_birth', 'province', 'city', 'mobile_no',
                  'cnic_or_b_form', 'email', 'village', 'address', 'current_level_of_education',
                  'institution_interested_in', 'admission_fee_of_the_program', 'total_fee_of_the_program',
                  'account_expenses', 'living_expenses', 'food_and_necessities_expenses', 'transport_amount',
                  'other_amount', 'total_members_of_household', 'members_earning', 'income_per_month',
                  'expense_per_month', 'description_of_household', 'personal_statement', 'total_amount',
                  'program_interested_in', 'degree_document',
                  'transcript_document', 'income_statement_document', 'profile_picture']

    # def create(self, validated_data):
    #     degrees_data = validated_data.pop('degrees')
    #     application = Application.objects.create(**validated_data)
    #     for degree_data in degrees_data:
    #         Degree.objects.create(application=application, **degree_data)
    #     return application


class ApplicationCreateByAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'student', 'name', 'father_name', 'last_name', 'gender', 'date_of_birth', 'province', 'city',
                  'mobile_no',
                  'cnic_or_b_form', 'email', 'village', 'address', 'current_level_of_education',
                  'institution_interested_in', 'admission_fee_of_the_program', 'total_fee_of_the_program',
                  'account_expenses', 'living_expenses', 'food_and_necessities_expenses', 'transport_amount',
                  'other_amount', 'total_members_of_household', 'members_earning', 'income_per_month',
                  'expense_per_month', 'description_of_household', 'personal_statement', 'total_amount',
                  'program_interested_in', 'degree_document',
                  'transcript_document', 'income_statement_document', 'profile_picture', 'degree', 'status',
                  'verification_required']


class ApplicationUpdateByAdminSerializer(serializers.ModelSerializer):
    # # Specify required=False for file fields
    degree_document = serializers.FileField(required=False)
    transcript_document = serializers.FileField(required=False)
    income_statement_document = serializers.FileField(required=False)
    profile_picture = serializers.FileField(required=False)
    degree = DegreeSerializer(many=True)

    class Meta:
        model = Application
        # fields = "__all__"
        fields = ['id', 'student', 'name', 'father_name', 'last_name', 'gender', 'date_of_birth', 'age', 'province',
                  'city',
                  'mobile_no',
                  'cnic_or_b_form', 'email', 'village', 'address', 'current_level_of_education',
                  'institution_interested_in', 'admission_fee_of_the_program', 'total_fee_of_the_program',
                  'account_expenses', 'living_expenses', 'food_and_necessities_expenses', 'transport_amount',
                  'other_amount', 'total_members_of_household', 'members_earning', 'income_per_month',
                  'expense_per_month', 'description_of_household', 'personal_statement', 'total_amount',
                  'program_interested_in', 'degree_document',
                  'transcript_document', 'income_statement_document', 'profile_picture', 'degree', 'status',
                  'verification_required']

    def update(self, instance, validated_data):
        # Update the instance fields
        instance.student = validated_data.get('student', instance.student)
        instance.name = validated_data.get('name', instance.name)
        instance.father_name = validated_data.get('father_name', instance.father_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.age = validated_data.get('age', instance.age)
        instance.province = validated_data.get('province', instance.province)
        instance.city = validated_data.get('city', instance.city)
        instance.cnic_or_b_form = validated_data.get('cnic_or_b_form', instance.cnic_or_b_form)
        instance.email = validated_data.get('email', instance.email)
        instance.village = validated_data.get('village', instance.village)
        instance.address = validated_data.get('address', instance.address)
        instance.current_level_of_education = validated_data.get('current_level_of_education',
                                                                 instance.current_level_of_education)
        instance.institution_interested_in = validated_data.get('institution_interested_in',
                                                                instance.institution_interested_in)
        instance.admission_fee_of_the_program = validated_data.get('admission_fee_of_the_program',
                                                                   instance.admission_fee_of_the_program)
        instance.total_fee_of_the_program = validated_data.get('total_fee_of_the_program',
                                                               instance.total_fee_of_the_program)
        instance.account_expenses = validated_data.get('account_expenses', instance.account_expenses)
        instance.living_expenses = validated_data.get('living_expenses', instance.living_expenses)
        instance.food_and_necessities_expenses = validated_data.get('food_and_necessities_expenses',
                                                                    instance.food_and_necessities_expenses)
        instance.transport_amount = validated_data.get('transport_amount', instance.transport_amount)
        instance.other_amount = validated_data.get('other_amount', instance.other_amount)
        instance.total_members_of_household = validated_data.get('total_members_of_household',
                                                                 instance.total_members_of_household)
        instance.members_earning = validated_data.get('members_earning', instance.members_earning)
        instance.income_per_month = validated_data.get('income_per_month', instance.income_per_month)
        instance.expense_per_month = validated_data.get('expense_per_month', instance.expense_per_month)
        instance.description_of_household = validated_data.get('description_of_household',
                                                               instance.description_of_household)
        instance.personal_statement = validated_data.get('personal_statement', instance.personal_statement)
        instance.total_amount = validated_data.get('total_amount', instance.total_amount)
        instance.program_interested_in = validated_data.get('program_interested_in', instance.program_interested_in)
        instance.total_amount = validated_data.get('total_amount', instance.total_amount)
        instance.verification_required = validated_data.get('verification_required', instance.verification_required)
        instance.status = validated_data.get('status', instance.status)

        instance.save()
        return instance

    # def update(self, instance, validated_data):
    #     # Get existing file values from instance
    #     existing_degree_document = instance.degree_document
    #     existing_transcript_document = instance.transcript_document
    #     existing_income_statement_document = instance.income_statement_document
    #     existing_profile_picture = instance.profile_picture
    #
    #     # Update validated data with existing file values if new files are not provided or are null
    #     validated_data.setdefault('degree_document', existing_degree_document)
    #     validated_data.setdefault('transcript_document', existing_transcript_document)
    #     validated_data.setdefault('income_statement_document', existing_income_statement_document)
    #     validated_data.setdefault('profile_picture', existing_profile_picture)
    #
    #     return super().update(instance, validated_data)


class BankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetails
        fields = ['id', 'account_title', 'IBAN_number', 'bank_name', 'branch_address', 'city']


class ProjectionSheetSerializer(serializers.ModelSerializer):
    results = ResultSerializer()
    other_documents = OtherDocumentSerializer()

    class Meta:
        model = ProjectionSheet
        fields = '__all__'


# --------------------------------student---------------------------------

class StudentSerializer(serializers.ModelSerializer):
    applications = ApplicationSerializer(many=True)
    projections = ProjectionSheetSerializer(many=True)
    bankdetails = BankDetailsSerializer(many=True)

    class Meta:
        model = Student
        fields = '__all__'


class StudentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class CreateStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['user', 'student_name', 'father_name', 'last_name', 'gender']


from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


# _____________________________________________verification serializer_________________________________________________
class VerificationsSerializer(serializers.ModelSerializer):
    application = ApplicationSerializer()

    class Meta:
        model = Verification
        fields = '__all__'


class VerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verification
        fields = ['application', 'verifier_name', 'verifier_email', 'verifier_contact', 'verification_date',
                  'verification_method', 'recommendation', 'move_for_interview']


# ------------------------------------------------interview serializer-----------------------------------------------
class InterviewsSerializer(serializers.ModelSerializer):
    application = ApplicationSerializer()

    class Meta:
        model = Interview
        fields = '__all__'


class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = ['application', 'interviewer_name', 'interview_date', 'question_1',
                  'question_2', 'question_3', 'question_4', 'question_5', 'question_6',
                  'question_7', 'question_8', 'question_9', 'question_10', 'question_11',
                  'interviewer_recommendation', 'Accepted']


# ------------------------------------------------------donor--------------------------------
class DonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = '__all__'


# --------------------------------------------------select Donor ------------------------------------------------------
class SelectDonorsSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    donor = DonorSerializer()

    class Meta:
        model = SelectDonor
        fields = '__all__'


class SelectDonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectDonor
        fields = '__all__'


# ------------------------------------------------------Mentor--------------------------------
class MentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = '__all__'


# --------------------------------------------------select Mentor ------------------------------------------------------
class SelectMentorsSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    mentor = MentorSerializer()

    class Meta:
        model = SelectMentor
        fields = '__all__'


class SelectMentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectMentor
        fields = '__all__'


# -------------------------------Projection serializer for admin -------------------------------------------


class ResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Results
        fields = ['result']


class DocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = ['documents']


class ProjectionSheetSerializers(serializers.ModelSerializer):
    # Define fields for handling file uploads
    challan = serializers.FileField(required=False)
    reciept = serializers.FileField(required=False)

    class Meta:
        model = ProjectionSheet
        fields = '__all__'


class ProjectionSheetSerializerss(serializers.ModelSerializer):
    results = serializers.FileField(required=False)
    other_documents = serializers.FileField(required=False)

    class Meta:
        model = ProjectionSheet
        fields = '__all__'

    def update(self, instance, validated_data):
        results_file = validated_data.pop('results', None)
        other_documents_file = validated_data.pop('other_documents', None)

        # Update the instance with other fields
        instance = super().update(instance, validated_data)

        # Handle file uploads for results
        if results_file:
            if instance.results:
                instance.results.result = results_file
                instance.results.save()
            else:
                results_instance = Results.objects.create(result=results_file)
                instance.results = results_instance

        # Handle file uploads for other_documents
        if other_documents_file:
            if instance.other_documents:
                instance.other_documents.documents = other_documents_file
                instance.other_documents.save()
            else:
                documents_instance = Documents.objects.create(documents=other_documents_file)
                instance.other_documents = documents_instance

        return instance


# -------------------------------------------------------donor and mentor  cration -----
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']  # Add other fields as needed
        extra_kwargs = {'password': {'write_only': True}}  # Password should not be read


class DonorsSerializer(serializers.ModelSerializer):
    # donor_username = UserSerializer(required=True)

    class Meta:
        model = Donor
        fields = ['donor_username', 'donor_name', 'donor_cnic', 'donor_contact', 'donor_email', 'donor_country']


class MentorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = ['mentor_username', 'mentor_name', 'mentor_cnic', 'mentor_contact', 'mentor_email', 'mentor_Expertise',
                  'mentor_country']
