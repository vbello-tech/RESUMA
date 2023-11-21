from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DetailView, View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import auth
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, update_session_auth_hash
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


# Create your views here.


# AUTHORIZATION
def signup_view(request):
    if request.method == 'POST':
        form = NewUSerForm(request.POST)
        if form.is_valid():
            user = form.save()
            Userprofile.objects.create(user=user)
            return redirect('user:create_profile')
    else:
        form = NewUSerForm()

    context = {
        'form': form
    }
    return render(request, 'registrations/signup.html', context)


class UserLogin(View):
    def get(self, *args, **kwargs):
        form = LoginForm()
        context = {
            'form': form,
        }
        return render(self.request, 'registrations/login.html', context)

    def post(self, backend='django.contrib.auth.backends.ModelBackend', *args, **kwargs):
        form = LoginForm(self.request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(self.request, username=username, password=password)
            if user:
                auth.login(self.request, user)
                return redirect('resume:home')
            else:
                return redirect('user:login')
        else:
            return redirect('user:login')


class CreateProfileView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            if Userprofile.objects.get(user=self.request.user, has_profile=True):
                return redirect('user:profile_edit')
        except ObjectDoesNotExist:
            context = {
                'form': ProfileForm(),
            }
            return render(self.request, 'resume/createprofile.html', context)

    def post(self, *args, **kwargs):
        user_p = Userprofile.objects.get(user=self.request.user)
        try:
            form = ProfileForm(self.request.POST or None)
            if form.is_valid():
                bio = form.cleaned_data.get('bio')
                phone = form.cleaned_data.get('phone')
                github = form.cleaned_data.get('github')
                experience_year = form.cleaned_data.get('experience_year')
                portfolio = form.cleaned_data.get('portfolio')
                linkedin = form.cleaned_data.get('linkedin')
                user_p.bio = bio
                user_p.phone = phone
                user_p.github = github
                user_p.experience_year = experience_year
                user_p.portfolio = portfolio
                user_p.linkedin = linkedin
                user_p.has_profile = True
                user_p.save()
                return redirect('user:user_detail', pk=self.request.user.pk)
            else:
                return redirect('user:sign_up')
        except ObjectDoesNotExist:
            return redirect('user:sign_up')


def logout(request):
    auth.logout(request)
    return redirect('resume:home')


@login_required
def user_edit(request, pk):
    d_user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = EditUserForm(request.POST, instance=d_user)
        if form.is_valid:
            user = form.save(commit=False)
            user.user = request.user
            user.save()
            return redirect('user:user_detail', pk=user.pk)
        form = EditUserForm()
    else:
        form = EditUserForm(instance=d_user)

    context = {
        'form': form
    }
    return render(request, 'registrations/user_edit.html', context)


@login_required
def profile_edit(request):
    user_profile = get_object_or_404(Userprofile, user=request.user)
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=user_profile)
        if form.is_valid:
            user = form.save(commit=False)
            user.user = request.user
            user.created_date = timezone.now()
            user.save()
            return redirect('user:user_detail', pk=request.user.pk)
        form = EditProfileForm()
    else:
        form = EditProfileForm(instance=user_profile)

    context = {
        'form': form
    }
    return render(request, 'registrations/profile_edit.html', context)


class UserDetailView(DetailView, LoginRequiredMixin):
    model = User
    template_name = "registrations/user_detail.html"


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('user:user_detail')
    else:
        form = PasswordChangeForm(data=request.POST, user=request.user)

    context = {
        'form': form
    }
    return render(request, 'registrations/change_password.html', context)
