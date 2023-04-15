from django import forms
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Userprofile
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget, PhoneNumberPrefixWidget
from datetime import datetime

Field_chioce = (
    ('BSC SCIENCE', 'BSC SCIENCE'),
    ('BSC ENGINEERING', 'BSC ENGINEERING'),
    ('BSC FINANCE', 'BSC FINANCE'),
    ('BSC ECONOMICS AND BUSINESS', 'BSC ECONOMICS AND BUSINESS'),
    ('BSC APPLIED SCIENCES', 'BSC APPLIED SCIENCES'),
    ('BOOTCAMP', 'BOOTCAMP'),
    ('BSC LAW', 'BSC LAW'),
)


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ('name',)

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    "placeholder": 'NAME OF THE POSITION YOU ARE APLLYING TO WITH THIS RESUME,. e.g, FULLSTACK DEVELOPER, BACKEND DEVELOPER',
                }
            )
        }

class SkillsForm(forms.Form):
    tech = forms.ModelMultipleChoiceField(
        required=False,
        queryset = Tech.objects.all(),
        initial=0,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'mt-2 mb-3 focus:border-blue-600 px-3',})
    )


class EducationForm(forms.Form):
    school_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        "placeholder": 'NAME OF THE SCHOOL YOU ATTENED',
    }))

    location = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        "placeholder": 'SCHOOL LOCATION',
    }))

    course = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        "placeholder": 'COURSES OF STUDY',
    }))

    field = forms.ChoiceField(
        required=False,
        choices=Field_chioce,
        initial=0,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'mt-2 mb-3 focus:border-blue-600 px-3', })
    )

    enrollment_date = forms.DateField(required=False, widget=forms.SelectDateWidget(empty_label=('Year', 'Month', 'Day'),
        years=range(1990, datetime.now().year),
        attrs={
            'data-date-format': 'dd/mm/yyyy',
            "placeholder": 'FORMAT YYYY-MM-DD (2002-02-20)',
    }))

    graduation_date = forms.DateField(required=False, widget=forms.SelectDateWidget(empty_label=('Year', 'Month', 'Day'),
        years=range(1990, datetime.now().year),
        attrs={
            'data-date-format': 'dd/mm/yyyy',
            "placeholder": 'FORMAT YYYY-MM-DD (2002-02-20)',
    }))

class ProjectForm(forms.Form):
    name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        "placeholder": 'PROJECT NAME',
    }))

    description = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        "placeholder": 'PROJECT DESCRIPTION',
        'rows': 3,
    }))

    github = forms.URLField(required=False, widget=forms.URLInput(attrs={
        'class': 'form-control',
        "placeholder": 'PROJECT SOURCE CODE',
    }))

    link = forms.URLField(required=False, widget=forms.URLInput(attrs={
        'class': 'form-control',
        "placeholder": 'PROJECT LINK',
    }))


class WorkForm(forms.Form):
    company_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        "placeholder": 'COMPANY NAME',
    }))

    role = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        "placeholder": 'YOUR ROLE IN THE COMPANY',
    }))

    company_description = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        "placeholder": 'A BRIEF DESCRIPTION OF WHAT THE COMAPNY IS.',
        'rows': 3,
    }))

    start_date = forms.DateField(required=False, widget=forms.SelectDateWidget(empty_label=('Year', 'Month', 'Day'),
        years=range(1990, datetime.now().year),
        attrs={
            'data-date-format': 'dd/mm/yyyy',
    }))

    end_date = forms.DateField(required=False, widget=forms.SelectDateWidget(empty_label=('Year', 'Month', 'Day'),
        years=range(1990, datetime.now().year + 1),
        attrs={
            'data-date-format': 'dd/mm/yyyy',
    }))


class NewUSerForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUSerForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()
        return user

class EditUserForm(UserChangeForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")

    def save(self, commit=True):
        user = super(EditUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()
        return user


class ProfileForm(forms.Form):
    bio = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'ABOUT YOU',
        'aria-describedby': 'basic-addon2',
        'rows': 5,
    }))
    phone = PhoneNumberField(required=False, widget=PhoneNumberPrefixWidget(
        initial='NG',
         attrs={
            'class': 'form-control',
            'placeholder': 'PHONE NUMBER',
            'aria-describedby': 'basic-addon2'
        }
    ))
    portfolio = forms.URLField(required=False, widget=forms.URLInput(attrs={
        'class': 'form-control',
        'placeholder': 'PORTFOLIO LINK',
        'aria-describedby': 'basic-addon2'
    }))
    github = forms.URLField(required=False, widget=forms.URLInput(attrs={
        'class': 'form-control',
        'placeholder': 'GITHUB PROFILE LINK',
        'aria-describedby': 'basic-addon2'
    }))
    linkedin = forms.URLField(required=False, widget=forms.URLInput(attrs={
        'class': 'form-control',
        'placeholder': 'LINKEDIN PROFILE LINK',
        'aria-describedby': 'basic-addon2'
    }))

class EditProfileForm(forms.ModelForm):

    class Meta:
        model = Userprofile
        fields = ('bio', 'phone', 'portfolio', 'github', 'linkedin',)

        widgets = {
            'phone': PhoneNumberPrefixWidget(
                initial='NG',
                attrs={
                    'class': 'form-control',
                    'placeholder': 'PHONE NUMBER',
                    'aria-describedby': 'basic-addon2'
                }
            )
        }


class LoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'USERNAME',
    }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'placeholder': 'PASSWORD',
    }))





