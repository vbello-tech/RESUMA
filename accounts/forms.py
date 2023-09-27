from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Userprofile
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget, PhoneNumberPrefixWidget


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
    experience_year = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'How many years experience do you have',
        'aria-describedby': 'basic-addon2'
    }))
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
