from django import forms
from django.forms import inlineformset_factory
from .models import Application, Degree, Donor, ProjectionSheet


# class ApplicationForm(forms.ModelForm):
#     class Meta:
#         model = Application
#         fields = ['name', 'father_name', 'last_name', 'gender', 'date_of_birth', 'age', 'country', 'province',
#                   'city', 'mobile_no', 'email', 'village', 'address', 'level_of_education', 'program_interested_in',
#                   'institution_name', 'total_cost_of_program', 'accommodation_amount', 'living_amount',
#                   'transport_amount', 'other_amount', 'total_members_of_household', 'members_earning',
#                   'income_per_month', 'expense_per_month', 'total_amount', 'personal_statement']


# DegreeFormSet = inlineformset_factory(Application, Degree, form=DegreeForm, extra=1)




class ProjectionSheetForm(forms.ModelForm):
    class Meta:
        model = ProjectionSheet
        fields = '__all__'
