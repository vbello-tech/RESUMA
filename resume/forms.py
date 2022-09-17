from django import forms
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Userprofile
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget, PhoneNumberPrefixWidget


class ResumeForm(forms.Form):
    name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        "placeholder": 'e.g BACKEND DEVELOPER, FULLSTACK DEVELOPER',
    }))

    school_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        "placeholder": 'NAME OF THE SCHOOL YOU ATTENED',
    }))

    location = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        "placeholder": 'SCHOOL LOCATION',
    }))

    field = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        "placeholder": 'FIELD OF STUDY',
    }))

    course = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        "placeholder": 'COURSES OF STUDY',
    }))

    name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        "placeholder": 'e.g BACKEND DEVELOPER, FULLSTACK DEVELOPER',
    }))

    enrollment_date = forms.DateField(required=False, widget=forms.DateInput(attrs={
        'class': 'form-control',
        "placeholder": 'FORMAT YYYY-MM-DD (2002-02-20)',
    }))

    graduation_date = forms.DateField(required=False, widget=forms.DateInput(attrs={
        'class': 'form-control',
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

    experience = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        "placeholder": 'TELL US SOME EXPERIENCE YOU GAINED WHILE WORKING ON THIS PROJECT',
        'rows': 3,
    }))


class WorkForm(forms.Form):
    company_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        "placeholder": 'COMPANY NAME',
    }))

    company_description = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        "placeholder": 'A BRIEF DESCRIPTION OF WHAT THE COMAPNY IS.',
        'rows': 3,
    }))

    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={
        'class': 'form-control',
        "placeholder": 'FORMAT YYYY-MM-DD (2002-02-20)',
    }))

    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={
        'class': 'form-control',
        "placeholder": 'FORMAT YYYY-MM-DD (2002-02-20)',
    }))

    responsibility = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        "placeholder": 'TELL US SOME OF YOUR RESPONSIBILITY AND EXPERIENCE WHILE WORKING IN THIS COMPANY',
        'rows': 3,
    }))


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ('body',)

        widgets = {
            'body': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    "placeholder": 'e.g I WORKED WITH AND LEARNT HOW TO USE STRIPE PAYMENT API',
                    'rows': 5,
                }
            )
        }


class ResponsibilityForm(forms.ModelForm):
    class Meta:
        model = Responsibility
        fields = ('body',)

        widgets = {
            'body': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    "placeholder": 'Enter your comment here',
                    'rows': 5,
                }
            )
        }

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
    bio = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'ABOUT YOU',
        'aria-describedby': 'basic-addon2'
    }))
    phone = PhoneNumberField(required=False, widget=PhoneNumberPrefixWidget(attrs={
        'class': 'form-control',
        'placeholder': 'PHONE NUMBER',
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
        fields = ('bio', 'phone', 'github', 'linkedin',)


class LoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'USERNAME',
    }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'PASSWORD',
    }))





