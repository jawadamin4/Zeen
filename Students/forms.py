from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from .models import Application, Degree, Donor, ProjectionSheet
from django.contrib.auth.forms import UserCreationForm
from .models import Student, Application

user = get_user_model()


class StudentRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="confirm password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = user
        fields = ['username', 'email', 'password1', 'password2']


class StudentInfoForm(forms.ModelForm):
    student_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    father_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Student
        fields = ['student_name', 'father_name', 'gender', ]


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


class login_form(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        exclude = ['student','degrees','status','verification_required']  # Add other fields you want to exclude

        widgets = {
            'date_of_birth': forms.TextInput(attrs={'class': 'datepicker'}),
        }

class DegreesForm(forms.ModelForm):
    class Meta:
        model = Degree
        fields = '__all__'
        exclude = ['application']