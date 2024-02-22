# zeen_app/urls.py

from django.urls import path, include
# from .views import student_profile, update_degree, update_student_info, donor_portal, student_detail, home,StudentListCreateView, StudentRetrieveUpdateDestroyView
# from .views import home, view_projection_sheet
# urlpatterns = [
#     path('', home, name='home'),
#     # path('student/<int:student_id>/', student_profile, name='student_profile'),
#     # path('degree/<int:degree_id>/update/', update_degree, name='update_degree'),
#     # path('student/portal/<int:student_id>', student_profile, name='student_portal'),
#     # path('student/update/', update_student_info, name='update_student_info'),
#     # path('donor/portal/', donor_portal, name='donor_portal'),
#     # path('donor/student/<int:student_id>/', student_detail, name='student_detail'),
#     # path('api/students/', StudentListCreateView.as_view(), name='student-list'),
#     # path('api/students/<int:pk>/', StudentRetrieveUpdateDestroyView.as_view(), name='student-details'),
#     # Add other URLs as needed
# ]
from rest_framework.routers import DefaultRouter
from .views import ApplicationViewSet, projections_view, update_projection, register_student, login_view, home, \
    studentDashboard, apply_for_scholarship, mentorDashboard, donorDashboard, LoginView, LogoutView, ProgramMV, \
    ApplicationsCV, ApplicationsReview, donor_panel, StudentDetailsView, ChallanUploadView, \
    ReceiptUploadView, ResultsUploadView, OtherDocumentsUploadView, CreateApplicationAPIView, CreateDegreeAPIView, \
    BankDetailsAPIView, ApplicationListView, StudentListAPIView, ProgramListAPIView, CreateApplicationByAdminAPIView, \
    UpdateDeleteApplicationByAdminAPIView, VerificationListView, VerificationCreateView, VerificationUpdateView, \
    VerificationDeleteView, VerificationRetrieveView, InterviewListCreateAPIView, InterviewRetrieveUpdateDestroyAPIView, \
    InterviewCreateView, SelectDonorRetrieveUpdateDestroy, SelectDonorListCreate, SelectDonorCreateView, \
    DonorListCreate, MentorListCreate, SelectMentorListCreate, SelectMentorCreateView, \
    SelectMentorRetrieveUpdateDestroy, ProgramListCreate, ProgramCreateView, ProgramRetrieveUpdateDestroy, \
    ProjectionSheetView, ProjectionSheetDetailView, ProjectionSheetDeleteView, StudentDeleteAPIView, StudentCreateView, \
    StudentEditView, UserDetailView, UserListAPIView, UpdateDeleteApplicationsByAdminAPIView, \
    DegreeViewSet, DonorCreateAPIView, MentorCreateAPIView, DegreeUpdateViewSet

router = DefaultRouter()
router.register(r'newapplications', ApplicationViewSet, basename='application')
# router.register(r'degrees', DegreeViewSet, basename='degree')
# router.register(r'programs',ProgramMV.as_view(),basename='programs')

urlpatterns = [

    path('api/', include(router.urls)),
    path('', home, name='home'),
    path('register_student/', register_student, name='register_student'),
    path('student_dashboard/', studentDashboard, name='student_dashboard'),
    path('apply_for_scholarship/', apply_for_scholarship, name='apply_for_scholarship'),
    path('login/', login_view, name='login'),
    path('admin-student-projections/<int:id>/', projections_view, name='admin-student-projections'),
    path('<int:student_id>/update-projection/<int:projection_id>/', update_projection, name='update-projection'),

    # metor dashboard urls
    path('mentor_dashboard/', mentorDashboard, name='mentor_dashboard'),

    # donor dashboard urls
    path('donor_dashboard/', donorDashboard, name='donor_dashboard'),

    # auth serialixers url
    path('loginn/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # add application api
    path('students/', StudentListAPIView.as_view(), name='student-list'),
    path('programs/', ProgramListAPIView.as_view(), name='program-list'),
    path('api/programs/', ProgramMV.as_view(), name='programs'),
    # path('api/applications/', ApplicationViewSet, name='applications'),
    path('api/create-application/', CreateApplicationAPIView.as_view(), name='create_application'),
    path('api/create-degree/', CreateDegreeAPIView.as_view(), name='create_degree'),
    # path('api/update-degree/', DegreeUpdateViewSet, name='update_degree'),

    path('api/application/<int:application_id>/degrees/', DegreeViewSet.as_view({'get': 'list'}), name='get_degree'),
    # URL for updating a specific degree
    path('api/application/<int:application_id>/degrees/<int:pk>/', DegreeViewSet.as_view({'put': 'update'}), name='update_degree'),

    # path('apii/applications/<int:pk>', ApplicationsReview.as_view(), name='programs'),
    path('api/bankDetails/', BankDetailsAPIView.as_view(), name='bankdetails-api'),

    # donorpanel
    path('api/donorStudents/', donor_panel, name="donor_students"),
    path('api/studentDetails/<int:id>/', StudentDetailsView.as_view(), name='student-details'),

    # projection sheet url for student
    path('api/upload/challan/<int:projection_id>/', ChallanUploadView.as_view(), name='upload_challan'),
    path('api/upload/reciept/<int:projection_id>/', ReceiptUploadView.as_view(), name='upload_receipt'),
    path('api/upload/results/<int:projection_id>/', ResultsUploadView.as_view(), name='upload_results'),
    path('api/upload/other_documents/<int:projection_id>/', OtherDocumentsUploadView.as_view(),
         name='upload_other_documents'),

    # adminDashboard_urls
    path('all-applications/', ApplicationListView.as_view(), name='application-list'),
    path('api/create-application-by-admin/', CreateApplicationByAdminAPIView.as_view(), name='create_application'),
    path('api/application/<int:pk>/', UpdateDeleteApplicationByAdminAPIView.as_view(),
         name='update-delete-application'),
    path('api/applications/<int:application_id>/', UpdateDeleteApplicationsByAdminAPIView.as_view(),
         name='update-delete-application'),

    # verification_URLS
    path('api/verifications/', VerificationListView.as_view(), name='verification-list'),
    path('api/verifications/create/', VerificationCreateView.as_view(), name='verification-create'),
    path('api/verifications/<int:id>/', VerificationRetrieveView.as_view(), name='verification-retrieve'),
    path('api/verifications/update/<int:id>/', VerificationUpdateView.as_view(), name='verification-update'),
    path('api/verifications/delete/<int:id>/', VerificationDeleteView.as_view(), name='verification-delete'),

    # interviews_urls
    path('api/interviews/', InterviewListCreateAPIView.as_view(), name='interview-list'),
    path('api/interview/create/', InterviewCreateView.as_view(), name='create-interview'),
    path('api/interviews/<int:pk>/', InterviewRetrieveUpdateDestroyAPIView.as_view(), name='interview-detail'),

    # donor-urls
    path('api/donor/', DonorListCreate.as_view(), name='donor-list'),

    # select donor urls
    path('api/select-donor/', SelectDonorListCreate.as_view(), name='select-donor-list'),
    path('api/select-donor/create/', SelectDonorCreateView.as_view(), name='create-select-donor'),
    path('api/select-donor/<int:pk>/', SelectDonorRetrieveUpdateDestroy.as_view(), name='select-donor-detail'),

    # mentor-urls
    path('api/mentor/', MentorListCreate.as_view(), name='mentor-list'),

    # select mentor urls
    path('api/select-mentor/', SelectMentorListCreate.as_view(), name='select-mentor-list'),
    path('api/select-mentor/create/', SelectMentorCreateView.as_view(), name='create-mentor-donor'),
    path('api/select-mentor/<int:pk>/', SelectMentorRetrieveUpdateDestroy.as_view(), name='select-mentor-detail'),

    # Programs urls
    path('api/Programs/', ProgramListCreate.as_view(), name='Programs-list'),
    path('api/Programs/create/', ProgramCreateView.as_view(), name='create-Programs'),
    path('api/Programs/<int:pk>/', ProgramRetrieveUpdateDestroy.as_view(), name='Programs-detail'),

    # projection-admin
    path('api/projections/', ProjectionSheetView.as_view(), name='projection-list'),
    path('api/projections/<int:projection_id>/', ProjectionSheetDetailView.as_view(), name='projection-detail'),
    path('api/projections/<int:projection_id>/delete/', ProjectionSheetDeleteView.as_view(), name='projection-delete'),

    # students
    path('api/students/create/', StudentCreateView.as_view(), name='student-create'),
    path('api/students/edit/<int:pk>/', StudentEditView.as_view(), name='student-edit'),
    path('api/students/<int:student_id>/delete/', StudentDeleteAPIView.as_view(), name='student-delete'),

    # ------------------user----------------------------

    path('api/user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('api/user/', UserListAPIView.as_view(), name='user-detail'),

    # ------------------------donor creation----------------------
    path('api/donor-create/', DonorCreateAPIView.as_view(), name='user-detail'),

    # ------------------------mentor creation----------------------
    path('api/mentor-create/', MentorCreateAPIView.as_view(), name='user-detail'),
]
