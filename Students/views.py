# zeen_app/views.py
from io import BytesIO

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from openpyxl import load_workbook

from .forms import ProjectionSheetForm
from .models import Degree, Application, Student, ProjectionSheet

from rest_framework import generics, viewsets
from .serializers import ApplicationSerializer
from django.http import HttpResponse
from django.conf import settings
import os


#

#
def home(request):
    return render(request, 'Students/home.html')


def projections_view(request, id):
    student = Student.objects.get(pk=id)
    projections = ProjectionSheet.objects.filter(student=student)
    print(projections)
    context = {
        'student': student,
        'projections': projections,
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
class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer


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
