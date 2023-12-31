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
from .views import ApplicationViewSet, projections_view, update_projection

router = DefaultRouter()
router.register(r'applications', ApplicationViewSet, basename='application')

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin-student-projections/<int:id>/', projections_view, name='admin-student-projections'),
    path('<int:student_id>/update-projection/<int:projection_id>/', update_projection, name='update-projection'),

]