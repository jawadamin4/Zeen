# admin.py in your Zeen app

from django.contrib import admin

from django.urls import reverse, path
from django.utils.html import format_html

from import_export.admin import ImportExportModelAdmin


from .models import Application, Degree, Verification, Interview, ProjectionSheet, SelectDonor, Student, Donor, Program
from .views import projections_view


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('username',
                    'student_name', 'father_name', 'last_name', 'gender', 'date_of_birth', 'age', 'country', 'province',
                    'city', 'mobile_no',
                    'email', 'village', 'address', 'view_projections_button')

    # actions = ['view_projections']

    def view_projections_button(self, obj):
        url = reverse('admin-student-projections', args=[obj.pk])
        return format_html('<a class="button" href="{}">View Projections</a>', url)

    view_projections_button.short_description = 'Projection sheets'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<id>/projections/', self.admin_site.admin_view(projections_view), name='admin-student-projections'),
        ]
        return custom_urls + urls


class DegreeAdmin(admin.ModelAdmin):
    list_display = ['application_name', 'degree_name', 'status', 'institute_name', 'grade']

    def application_name(self, obj):
        return obj.application.name


class VerificationAdmin(admin.ModelAdmin):
    list_display = ['application_name', 'verifier_name', 'verification_date', 'status']
    readonly_fields = ['status']

    def application_name(self, obj):
        return obj.application.name


class DegreeInline(admin.TabularInline):
    model = Degree


class VerificationInline(admin.TabularInline):
    model = Verification
    extra = 1


class ApplicationAdmin(admin.ModelAdmin):
    inlines = [DegreeInline]
    fieldsets = (
        ('Application Status', {
            'fields': ('status', 'verification_required'),
        }),
        ('Personal Information', {
            'fields': ('name', 'father_name', 'last_name', 'date_of_birth', 'age', 'gender'),
        }),
        ('Contact Information', {
            'fields': ('mobile_no', 'cnic_or_b_form', 'email', 'country', 'province', 'city', 'village', 'address'),
        }),
        ('Education Information', {
            'fields': ('current_level_of_education', 'program_interested_in', 'institution_interested_in'),
        }),

        ('Financial Information', {
            'fields': (
                'admission_fee_of_the_program', 'total_fee_of_the_program', 'account_expenses', 'living_expenses',
                'food_and_necessities_expenses', 'transport_amount', 'other_amount'),
        }),
        ('Banking Details', {
            'fields': ('account_title', 'bank_account_number', 'bank_name'),
        }),
        ('Household Information', {
            'fields': (
                'total_members_of_household', 'description_of_household', 'members_earning', 'income_per_month',
                'expense_per_month',
                'total_amount'),
        }),
        ('Personal Statement', {
            'fields': ('personal_statement',),
        }),
        ('Document Uploads', {
            'fields': ('degree_document', 'transcript_document', 'income_statement_document', 'profile_picture'),
        }),

    )
    list_display = ['name', 'status']
    list_filter = ('status',)
    search_fields = ('name', 'status')
    readonly_fields = ['age', 'total_amount']


# Register your models and admin classes
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Degree, DegreeAdmin)
admin.site.register(Verification, VerificationAdmin)


class InterviewAdmin(admin.ModelAdmin):
    list_display = ('application', 'interviewer_name', 'interview_date',
                    'interviewer_recommendation', 'status')
    readonly_fields = ['status']
    fieldsets = [
        ('Interview Information', {
            'fields': ['application', 'interviewer_name', 'interview_date'],
        }),
        ('Questions', {
            'fields': [
                'question_1',
                'question_2',
                'question_3',
                'question_4',
                'question_5',
                'question_6',
                'question_7',
                'question_8',
                'question_9',
                'question_10',
                'question_11',
            ],
        }),
        ('Other Information', {
            'fields': ['interviewer_recommendation', 'Accepted', "status"],
        }),
    ]


admin.site.register(Interview, InterviewAdmin)


class ProjectionSheetAdmin(ImportExportModelAdmin):
    list_display = ['student', 'semester', 'tuition_fee', 'other_fee', 'total_cost', 'sponsor_name',
                    'sponsorship_commitment', 'fee_due_date', 'status', 'payment_date']
    list_filter = ['status', 'sponsorship_commitment']

    # def view_projection_sheet(self, obj):
    #     # Assuming you have an Application FK in ForecastEntry
    #
    #     filename = f'{obj.application.name}_projection_sheet.xlsx'
    #
    #     # Generate a link to the view_projection_sheet
    #     url = reverse('view_projection_sheet', args=[obj.pk,filename])
    #
    #     return format_html(f'<a href="{url}" target="_blank">{filename}</a>')
    #
    # view_projection_sheet.short_description = 'Projection Sheet'
    # view_projection_sheet.allow_tags = True  # Required for format_html
    # #
    # def view_projection_sheet(self, obj):
    #     # Assuming the Excel file is stored in a FileField named 'projection_sheet'
    #     filename = f'{obj.application.name}_projection_sheet.xlsx'
    #     excel_file_path = f'staticfiles/projections/{filename}'
    #
    #     try:
    #         wb = load_workbook(excel_file_path)
    #         # Assuming data is in the first sheet
    #         sheet = wb.active
    #         data = []
    #         for row in sheet.iter_rows(min_row=2, values_only=True):
    #             data.append(row)
    #
    #         # Extract headers from the first row
    #         headers = [cell.value for cell in sheet[1]]
    #
    #         # Render data in an HTML table
    #         table_html = '<table border="1"><tr>'
    #         for header in headers:
    #             table_html += f'<th>{header}</th>'
    #         table_html += '</tr>'
    #         for row in data:
    #             table_html += '<tr>'
    #             for cell in row:
    #                 table_html += f'<td>{cell}</td>'
    #             table_html += '</tr>'
    #         table_html += '</table>'
    #
    #         return mark_safe(table_html)
    #     except Exception as e:
    #         return f"Error: {str(e)}"
    #
    # view_projection_sheet.short_description = 'Projection Sheet'

    def application_name(self, obj):
        return obj.application.name

    application_name.admin_order_field = 'application__name'


admin.site.register(ProjectionSheet, ProjectionSheetAdmin)


class SelectDonorAdmin(admin.ModelAdmin):
    list_display = ('application', 'Donor', "selection_date")
    # search_fields = ('application__name', 'Donor__donor_name')  # Assuming you have a 'name' field in Application and 'donor_name' in Donor


admin.site.register(SelectDonor, SelectDonorAdmin)
admin.site.register(Program)
class DonorAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Donor information', {
            'fields': ['donor_name','donor_cnic', 'donor_contact','donor_email','donor_country'],
        })]
    list_display = ('donor_cnic', 'donor_contact', 'donor_email', 'donor_country')


admin.site.register(Donor, DonorAdmin)