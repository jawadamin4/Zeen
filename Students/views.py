# zeen_app/views.py
import secrets
import string
from copy import deepcopy
# from django.db import IntegrityError
from sqlite3 import IntegrityError

from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView, DestroyAPIView

from .forms import ProjectionSheetForm, StudentRegistrationForm, StudentInfoForm, login_form, ApplicationForm, \
    DegreesForm
from .models import Application, Student, ProjectionSheet, Program, SelectDonor, Donor, Results, Documents, BankDetails, \
    Degree, Verification, Interview, Mentor, SelectMentor
from rest_framework import viewsets, generics, status
from .serializers import ApplicationSerializer, StudentSerializer, ProjectionSheetSerializer, DegreeSerializer, \
    ApplicationCreateSerializer, BankDetailsSerializer, ProgramSerializers, ApplicationCreateByAdminSerializer, \
    VerificationSerializer, VerificationsSerializer, InterviewSerializer, InterviewsSerializer, SelectDonorSerializer, \
    DonorSerializer, SelectDonorsSerializer, MentorSerializer, SelectMentorsSerializer, SelectMentorSerializer, \
    ProjectionSheetSerializers, ProjectionSheetSerializerss, StudentSerializers, CreateStudentSerializer, \
    ApplicationUpdateByAdminSerializer, DonorsSerializer, MentorsSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, ProgramSerializer
from rest_framework.parsers import MultiPartParser, FormParser


#

#
def register_student(request):
    if request.method == 'POST':
        user_form = StudentRegistrationForm(request.POST)
        info_form = StudentInfoForm(request.POST)

        if user_form.is_valid() and info_form.is_valid():
            user = user_form.save()
            student = info_form.save(commit=False)
            student.user = user
            student.save()

            login(request, user)
            # Automatically log in the user after registration
            if hasattr(user, 'student'):
                return redirect('student_dashboard')
            elif hasattr(user, 'mentor'):
                return redirect('mentor_dashboard')
            elif hasattr(user, 'donor'):
                return redirect('donor_dashboard')
        else:
            messages.warning(request, "username already exists choose another username", extra_tags='error')
    else:
        user_form = StudentRegistrationForm()
        info_form = StudentInfoForm()

    return render(request, 'Students/studentRegistration.html',
                  {'user_form': user_form, 'info_form': info_form})


def home(request):
    return render(request, 'Students/home.html')


def projections_view(request, id):
    student = Student.objects.get(pk=id)
    projections = ProjectionSheet.objects.filter(student=student)
    projections_count = projections.count()
    is_semester_based = 1 <= projections_count <= 4 or 1 <= projections_count <= 8

    context = {
        'student': student,
        'projections': projections,
        'projections_count': projections_count,
        'is_semester_based': is_semester_based,
    }

    return render(request, 'Students/student_projections.html', context)


#
# def view_projection_sheet(request, pk, filename):
#     forecast_entry = ForecastEntry.objects.get(pk=pk)
#     # Construct the file path
#     unique_filename = f'{forecast_entry.application.name}_projection_sheet.xlsx'
#     print(unique_filename)
#     file_path = f'staticfiles/projections/{unique_filename}'
#
#     # Check if the file exists
#     if os.path.exists(file_path):
#         with open(file_path, 'rb') as file:
#             response = HttpResponse(file.read(),
#                                     content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#
#             # Set Content-Disposition for inline display
#             response['Content-Disposition'] = f'attachment; filename="{filename}"'
#
#         return response
#     else:
#         return HttpResponse(f"Projection sheet not available for filename: {filename}", status=404)
# # def view_projection_sheet(request, filename):
# #     excel_file_path = f'staticfiles/projections/{filename}'
# #
# #     try:
# #         # Load the Excel file
# #         wb = load_workbook(excel_file_path)
# #     except FileNotFoundError:
# #         # Handle the case where the file is not found
# #         return HttpResponse("Projection sheet not found", status=404)
# #
# #     # Create a BytesIO object to write the Excel file to memory
# #     output = BytesIO()
# #
# #     # Save the Excel file to the BytesIO object
# #     wb.save(output)
# #
# #     # Set the response content type for Excel files
# #     response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
# #     response['Content-Disposition'] = f'inline; filename={filename}'
#
#     return response
# class ApplicationViewSet(viewsets.ModelViewSet):
#     queryset = Application.objects.all()
#     serializer_class = ApplicationSerializer


def update_projection(request, student_id, projection_id):
    student = Student.objects.get(pk=student_id)
    projection = get_object_or_404(ProjectionSheet, pk=projection_id, student=student)

    if request.method == 'POST':
        form = ProjectionSheetForm(request.POST, instance=projection)
        if form.is_valid():
            form.save()
            return redirect('admin-student-projections', id=student_id)
    else:
        form = ProjectionSheetForm(instance=projection)

    context = {
        'form': form,
        'student': student,
    }
    return render(request, 'students/update_projection.html', context)


def login_view(request):
    form = login_form(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if hasattr(user, 'student'):
                    return redirect('student_dashboard')
                elif hasattr(user, 'mentor'):
                    return redirect('mentor_dashboard')
                elif hasattr(user, 'donor'):
                    print(user.donor)
                    return redirect('donor_dashboard')
            else:
                messages.warning(request, "username or password is incorrect", extra_tags='error')
    return render(request, 'Students/login.html', {'form': form})


def studentDashboard(request):
    # Assuming you have a one-to-one relationship between Student and User
    student = request.user.student

    # Retrieve applications submitted by the logged-in student
    applications = Application.objects.filter(student=student)

    return render(request, 'Students/student_dashboard.html', {'applications': applications})


def mentorDashboard(request):
    return render(request, 'Students/mentor_dashboard.html')


def donorDashboard(request):
    return render(request, 'Students/donor_dashboard.html')


def apply_for_scholarship(request):
    if request.method == 'POST':
        application_form = ApplicationForm(request.POST, request.FILES)
        degree_form = DegreesForm(request.POST)

        if application_form.is_valid() and degree_form.is_valid():
            application = application_form.save(commit=False)
            application.student = request.user.student
            application.save()

            degrees = degree_form.save(commit=False)
            degrees.application = application
            degrees.save()

            messages.success(request, 'Application submitted successfully.')
            return redirect('student_dashboard')
        else:
            messages.error(request, 'There were errors in your form. Please correct them.')
    else:
        application_form = ApplicationForm()
        degree_form = DegreesForm()

    return render(
        request,
        'Students/apply_for_scholarship.html',
        {'applicationForm': application_form, 'degreeForm': degree_form}
    )


from rest_framework.exceptions import ValidationError


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)

            # Check if the user is associated with a donor or a student
            if hasattr(user, 'donor'):
                donor_name = user.donor.donor_name
                user_data = {'token': token.key, 'user': UserSerializer(user).data, 'role': 'donor',
                             'donor_name': donor_name}
            elif hasattr(user, 'student'):
                studentId = user.student.id
                user_data = {'token': token.key, 'user': UserSerializer(user).data, 'role': 'student',
                             'studentId': studentId}
            else:
                user_data = {'token': token.key, 'user': UserSerializer(user).data}

            return Response(user_data)
        except ValidationError as e:
            # If validation error occurs, return a 400 Bad Request response with error details
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response({'detail': 'Successfully logged out'})


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def perform_create(self, serializer):
        # Check if the user is authenticated and has a 'student' attribute
        if hasattr(self.request.user, 'student'):
            student = self.request.user.student

            # Extract application data from the request data
            application_data = self.request.data

            # Extract degrees data from the application data
            degrees_data = application_data.pop('degrees', None)

            # If degrees data is provided, create the degree objects
            if degrees_data:
                degree_serializer = DegreeSerializer(data=degrees_data, many=True)
                if degree_serializer.is_valid():
                    degrees = degree_serializer.save()
                else:
                    return Response({'error': 'Invalid degree data.'},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Degrees data is missing.'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Save the application with the associated student and degrees
            serializer.save(student=student, degrees=degrees)
        else:
            return Response({'error': 'User does not have a valid student attribute.'},
                            status=status.HTTP_400_BAD_REQUEST)


class CreateApplicationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Extract the application data
        application_data = request.data

        # Create application instance
        serializer = ApplicationCreateSerializer(data=application_data)
        if serializer.is_valid():
            # Assuming the authenticated user is the student, you can customize this part as needed
            user = request.user
            student = user.student if hasattr(user, 'student') else None
            if not student:
                return Response({'error': 'User does not have a valid student attribute.'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Save the application with the associated student
            application = serializer.save(student=student)
            application_id = application.id

            return Response({'application_id': application_id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# by admin
class CreateApplicationByAdminAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Extract the application data
        application_data = request.data

        # Create application instance
        serializer = ApplicationCreateByAdminSerializer(data=application_data)
        if serializer.is_valid():
            # Assuming the authenticated user is the student, you can customize this part as needed
            # user = request.user
            # student = user.student if hasattr(user, 'student') else None
            # if not student:
            #     return Response({'error': 'User does not have a valid student attribute.'},
            #                     status=status.HTTP_400_BAD_REQUEST)

            # Save the application with the associated student
            application = serializer.save()
            application_id = application.id

            return Response({'application_id': application_id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# update delete by admin of applications
class UpdateDeleteApplicationByAdminAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationUpdateByAdminSerializer

    def put(self, request, *args, **kwargs):
        # Retrieve the application instance
        instance = self.get_object()

        # Partial update
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            print("Serializer Errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UpdateDeleteApplicationsByAdminAPIView(APIView):
    def put(self, request, application_id, *args, **kwargs):
        # Retrieve the application instance
        try:
            instance = Application.objects.get(id=application_id)
        except Application.DoesNotExist:
            return Response({"error": "Application not found"}, status=404)

        # Use request.FILES to access uploaded files
        print(request.data)
        degree_document = request.FILES.get('degree_document')
        transcript_document = request.FILES.get('transcript_document')
        income_statement_document = request.FILES.get('income_statement_document')
        profile_picture = request.FILES.get('profile_picture')

        # Save files to the server's file system
        if degree_document:
            instance.degree_document.save(degree_document.name, degree_document)
        if transcript_document:
            instance.transcript_document.save(transcript_document.name, transcript_document)
        if income_statement_document:
            instance.income_statement_document.save(income_statement_document.name, income_statement_document)
        if profile_picture:
            instance.profile_picture.save(profile_picture.name, profile_picture)

        data = request.data.copy()
        del data['degree_document']
        del data['transcript_document']
        del data['income_statement_document']
        del data['profile_picture']

        # Serialize the updated data
        serializer = ApplicationUpdateByAdminSerializer(instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def delete(self, request, application_id, *args, **kwargs):
        # Retrieve the application instance
        try:
            instance = Application.objects.get(id=application_id)
        except Application.DoesNotExist:
            return Response({"error": "Application not found"}, status=404)

        # Delete the application instance
        instance.delete()

        return Response({"message": "Application deleted successfully"})


class CreateDegreeAPIView(APIView):

    def handle_degree_data(self, degree_data, application_id):
        degrees = []
        for degree_item in degree_data:
            degree_item['application'] = application_id
            degree_serializer = DegreeSerializer(data=degree_item)
            if degree_serializer.is_valid():
                degree = degree_serializer.save()
                degrees.append(degree)
            else:
                return None, Response({'error': degree_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return degrees, None

    def post(self, request, *args, **kwargs):
        degree_data = request.data.get('degrees', [])
        application_id = request.data.get('application_id')
        degrees, error_response = self.handle_degree_data(degree_data, application_id)
        if error_response:
            return error_response
        return Response('success', status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        degree_data = request.data.get('degrees', [])
        application_id = request.data.get('application_id')
        print(application_id)

        # Retrieve the application instance
        application = Application.objects.get(id=application_id)

        # Update or create degree instances and associate them with the application
        degrees = []
        for degree_item in degree_data:
            degree_name = degree_item['degree_name']

            # Look for an existing degree associated with the application
            degree_instance = application.degrees.filter(degree_name=degree_name).first()

            # If the degree exists, update it; otherwise, create a new one
            if degree_instance:
                degree_serializer = DegreeSerializer(degree_instance, data=degree_item)
            else:
                # Assign application_id to the degree
                degree_item['application'] = application_id
                degree_serializer = DegreeSerializer(data=degree_item)

            if degree_serializer.is_valid():
                degree = degree_serializer.save()
                degrees.append(degree)
            else:
                return Response({'error': degree_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response('success', status=status.HTTP_201_CREATED)


class DegreeViewSet(viewsets.ViewSet):
    # Optionally, you can filter degrees by application ID
    def list(self, request, application_id=None):
        queryset = Degree.objects.filter(application_id=application_id)
        serializer = DegreeSerializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None, application_id=None):
        try:
            degree = Degree.objects.get(pk=pk)
        except Degree.DoesNotExist:
            return Response({"error": "Degree not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DegreeSerializer(degree, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DegreeUpdateViewSet(viewsets.ModelViewSet):
    queryset = Degree.objects.all()
    serializer_class = DegreeSerializer
    permission_classes = [IsAuthenticated]


# class CreateApplicationAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         # Extract the degree data from the request data
#
#         # Create application instance
#         serializer = ApplicationCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             # Assuming the authenticated user is the student, you can customize this part as needed
#             user = request.user
#             student = user.student if hasattr(user, 'student') else None
#             if not student:
#                 return Response({'error': 'User does not have a valid student attribute.'},
#                                 status=status.HTTP_400_BAD_REQUEST)
#
#             # Save the application with the associated student and degrees
#             application = serializer.save(student=student)
#
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApplicationListView(ListAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer


class ProgramMV(APIView):

    def get(self, request):
        programs = Program.objects.all()
        serializer = ProgramSerializer(programs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProgramSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ApplicationsCV(generics.ListCreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer


class ApplicationsReview(generics.RetrieveUpdateDestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer


# @api_view(['GET'])

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def donor_panel(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

    # Get the donor associated with the current user
    donor = get_object_or_404(Donor, donor_username=request.user)

    # Get all students associated with the donor
    select_donor_entries = SelectDonor.objects.filter(donor=donor)
    sponsored_students = [entry.student for entry in select_donor_entries]

    # Serialize the student data
    serializer = StudentSerializer(sponsored_students, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


class ChallanUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, projection_id, *args, **kwargs):
        try:
            projection = ProjectionSheet.objects.get(id=projection_id)
        except ProjectionSheet.DoesNotExist:
            return Response({'error': 'ProjectionSheet not found'}, status=status.HTTP_404_NOT_FOUND)

        challan_file = request.FILES.get('challan')
        if not challan_file:
            return Response({'error': 'Challan file not provided'}, status=status.HTTP_400_BAD_REQUEST)

        projection.challan = challan_file
        projection.save()

        return Response({'message': 'Challan uploaded successfully'}, status=status.HTTP_200_OK)


class ReceiptUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, projection_id, *args, **kwargs):
        try:
            projection = ProjectionSheet.objects.get(id=projection_id)
        except ProjectionSheet.DoesNotExist:
            return Response({'error': 'ProjectionSheet not found'}, status=status.HTTP_404_NOT_FOUND)

        receipt_file = request.FILES.get('reciept')
        if not receipt_file:
            return Response({'error': 'Receipt file not provided'}, status=status.HTTP_400_BAD_REQUEST)

        projection.reciept = receipt_file
        projection.save()

        return Response({'message': 'Receipt uploaded successfully'}, status=status.HTTP_200_OK)


class ResultsUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, projection_id, *args, **kwargs):
        try:
            projection = ProjectionSheet.objects.get(id=projection_id)
        except ProjectionSheet.DoesNotExist:
            return Response({'error': 'ProjectionSheet not found'}, status=status.HTTP_404_NOT_FOUND)

        results_file = request.FILES.get('results')
        if not results_file:
            return Response({'error': 'Results file not provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new Results instance with the provided file
        results_instance = Results.objects.create(result=results_file)

        # Assign the new Results instance to the ProjectionSheet
        projection.results = results_instance
        projection.save()

        return Response({'message': 'Results uploaded successfully'}, status=status.HTTP_200_OK)


class OtherDocumentsUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, projection_id, *args, **kwargs):
        try:
            projection = ProjectionSheet.objects.get(id=projection_id)
        except ProjectionSheet.DoesNotExist:
            return Response({'error': 'ProjectionSheet not found'}, status=status.HTTP_404_NOT_FOUND)

        other_documents_file = request.FILES.get('other_documents')
        if not other_documents_file:
            return Response({'error': 'Other Documents file not provided'}, status=status.HTTP_400_BAD_REQUEST)
        # Create a new documents instance with the provided file
        other_documents_instance = Documents.objects.create(documents=other_documents_file)
        projection.other_documents = other_documents_instance
        projection.save()

        return Response({'message': 'Other Documents uploaded successfully'}, status=status.HTTP_200_OK)


class BankDetailsAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Assuming that the student_id is provided in the request data
        student_id = request.data.get('student')
        try:
            student = Student.objects.get(pk=student_id)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        # Assign the student instance to the student field of the serializer
        serializer = BankDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(student=student)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        try:
            student_id = request.data.get('student')
            bank_details = BankDetails.objects.get(student_id=student_id)
        except BankDetails.DoesNotExist:
            return Response({"error": "Bank details not found for this student"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BankDetailsSerializer(bank_details, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ________________________________________verification view ________________________________________________________
class VerificationListView(generics.ListAPIView):
    queryset = Verification.objects.all()
    serializer_class = VerificationsSerializer


class VerificationCreateView(generics.CreateAPIView):
    serializer_class = VerificationSerializer


class VerificationRetrieveView(generics.RetrieveAPIView):
    queryset = Verification.objects.all()
    serializer_class = VerificationSerializer
    lookup_field = 'id'  # Assuming 'id' is the name of the primary key field

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VerificationUpdateView(generics.UpdateAPIView):
    queryset = Verification.objects.all()
    serializer_class = VerificationSerializer
    lookup_field = 'id'  # Assuming 'id' is the name of the primary key field


class VerificationDeleteView(generics.DestroyAPIView):
    queryset = Verification.objects.all()
    serializer_class = VerificationSerializer
    lookup_field = 'id'  # Assuming 'id' is the name of the primary key field


# ------------------------------------------------------interview serializer views-----------------------------------
class InterviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = Interview.objects.all()
    serializer_class = InterviewsSerializer


class InterviewCreateView(generics.CreateAPIView):
    serializer_class = InterviewSerializer


class InterviewRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer


# ------------------------------------------------donor---------------------------------------------------------------
class DonorListCreate(generics.ListCreateAPIView):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer


# --------------------------------------------select donor------------------------------------------------------------
class SelectDonorListCreate(generics.ListCreateAPIView):
    queryset = SelectDonor.objects.all()
    serializer_class = SelectDonorsSerializer


class SelectDonorCreateView(generics.CreateAPIView):
    serializer_class = SelectDonorSerializer


class SelectDonorRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = SelectDonor.objects.all()
    serializer_class = SelectDonorSerializer


# ------------------------------------------------mentor---------------------------------------------------------------
class MentorListCreate(generics.ListCreateAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer


# --------------------------------------------select mentor------------------------------------------------------------
class SelectMentorListCreate(generics.ListCreateAPIView):
    queryset = SelectMentor.objects.all()
    serializer_class = SelectMentorsSerializer


class SelectMentorCreateView(generics.CreateAPIView):
    serializer_class = SelectMentorSerializer


class SelectMentorRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = SelectMentor.objects.all()
    serializer_class = SelectMentorSerializer


# -----------------------------------------------------PROGRAMS-------------------------------------------------
class ProgramListCreate(generics.ListCreateAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializers


class ProgramListAPIView(generics.ListAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializers


class ProgramCreateView(generics.CreateAPIView):
    serializer_class = ProgramSerializers


class ProgramRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializers


# ------------------------------------------Projection view for admin ----------------------------------------------
class ProjectionSheetView(APIView):
    def get(self, request):
        projections = ProjectionSheet.objects.all()
        serializer = ProjectionSheetSerializers(projections, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Create a mutable copy of request.data
        mutable_data = deepcopy(request.data)

        # Extract data for related fields
        results_data = mutable_data.pop('results', None)
        other_documents_data = mutable_data.pop('other_documents', None)

        # Create instances for related fields
        results_instance = None
        if results_data:
            if isinstance(results_data, list):
                results_instance = Results.objects.create(result=results_data[0])
            else:
                results_instance = Results.objects.create(result=results_data)
        else:
            results_instance = Results.objects.create()  # Create empty instance if no data provided

        other_documents_instance = None
        if other_documents_data:
            if isinstance(other_documents_data, list):
                other_documents_instance = Documents.objects.create(documents=other_documents_data[0])
            else:
                other_documents_instance = Documents.objects.create(documents=other_documents_data)
        else:
            other_documents_instance = Documents.objects.create()  # Create empty instance if no data provided

        # Link related instances to ProjectionSheet model
        mutable_data['results'] = results_instance.id
        mutable_data['other_documents'] = other_documents_instance.id

        # Create ProjectionSheetSerializer instance
        serializer = ProjectionSheetSerializers(data=mutable_data)

        # Validate and save the serializer instance
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            projection_sheet = ProjectionSheet.objects.get(pk=pk)
        except ProjectionSheet.DoesNotExist:
            return Response({"error": "ProjectionSheet does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Extract file data for related fields
        results_file = request.FILES.get('results')
        other_documents_file = request.FILES.get('other_documents')

        # Update related instances if files are provided
        if results_file:
            # Create or update Results instance
            results_instance, created = Results.objects.get_or_create(projection_sheet=projection_sheet)
            results_instance.result = results_file
            results_instance.save()

            # Update projection_sheet with results_instance
            projection_sheet.results = results_instance

        if other_documents_file:
            # Create or update Documents instance
            documents_instance, created = Documents.objects.get_or_create(projection_sheet=projection_sheet)
            documents_instance.documents = other_documents_file
            documents_instance.save()

            # Update projection_sheet with documents_instance
            projection_sheet.other_documents = documents_instance

        # Serialize and save the updated projection_sheet
        serializer = ProjectionSheetSerializers(projection_sheet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectionSheetDetailView(RetrieveUpdateAPIView):
    queryset = ProjectionSheet.objects.all()
    serializer_class = ProjectionSheetSerializerss
    lookup_url_kwarg = 'projection_id'
    lookup_field = 'id'


class ProjectionSheetDeleteView(DestroyAPIView):
    queryset = ProjectionSheet.objects.all()
    lookup_url_kwarg = 'projection_id'
    lookup_field = 'id'


# --------------------------------student api view ----------------------------------------------
class StudentListAPIView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentDetailsView(generics.RetrieveAPIView):
    queryset = Student.objects.all()  # Replace with your actual queryset
    serializer_class = StudentSerializer
    lookup_field = 'id'  # Assuming you use 'id' as the lookup field, adjust if needed


class StudentDeleteAPIView(DestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_url_kwarg = 'student_id'

    def perform_destroy(self, instance):
        # Delete related objects (applications, projections, bank details)
        instance.applications.all().delete()
        instance.projections.all().delete()
        instance.bankdetails.all().delete()

        # Delete linked user if exists
        if instance.user:
            instance.user.delete()
        # Call super method to delete the student instance
        super().perform_destroy(instance)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class StudentCreateView(APIView):
    def post(self, request):
        serializer = CreateStudentSerializer(data=request.data)
        if serializer.is_valid():
            if User.objects.filter(username=serializer.validated_data['student_name']).exists():
                raise ValidationError("A user with this username already exists.")
            try:
                # Generate password based on student name
                password = serializer.validated_data['student_name'] + "123"
                # Create user with generated password
                user = User.objects.create(
                    username=serializer.validated_data['student_name'],
                    password=make_password(password)
                )
                # Save the student with the user instance
                serializer.save(user=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                # If a UNIQUE constraint violation occurs on the username field
                return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentEditView(APIView):
    def put(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response({"message": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentSerializers(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------------------user--------------
User = get_user_model()


class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
#------------------------------------------------

class DonorCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = DonorsSerializer(data=request.data)
        if serializer.is_valid():
            if User.objects.filter(username=serializer.validated_data['donor_name']).exists():
                raise ValidationError("A user with this username already exists.")

            try:
                # Generate password based on student name
                password = serializer.validated_data['donor_name'] + "123"
                # Create user with generated password
                user = User.objects.create(
                    username=serializer.validated_data['donor_name'],
                    password=make_password(password)
                )
                # Save the student with the user instance
                serializer.save(donor_username=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                # If a UNIQUE constraint violation occurs on the username field
                return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MentorCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MentorsSerializer(data=request.data)
        if serializer.is_valid():
            if User.objects.filter(username=serializer.validated_data['mentor_name']).exists():
                raise ValidationError("A user with this username already exists.")
            try:
                # Generate password based on student name
                password = serializer.validated_data['mentor_name'] + "123"
                # Create user with generated password
                user = User.objects.create(
                    username=serializer.validated_data['mentor_name'],
                    password=make_password(password)
                )
                # Save the student with the user instance
                serializer.save(mentor_username=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                # If a UNIQUE constraint violation occurs on the username field
                return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)