from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.views.generic import TemplateView, DetailView, View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, update_session_auth_hash

# Create your views here.


def home(request):
    context ={
        'user':request.user
    }
    return render(request, 'home.html', context)


class AddResumeView(View):
    def get(self, *args, **kwargs):
        form = ResumeForm()
        context = {
            'form': form,
        }
        return render (self.request, 'resume/addproject.html', context)

    def post(self, *args, **kwargs):
        try:
            form = ResumeForm(self.request.POST or None)
            if form.is_valid:
                body = form.save(commit=False)
                body.user = self.request.user
                body.save()
                return redirect('resume:add_project', pk=body.pk)
            else:
                return redirect('resume:home')

        except ObjectDoesNotExist:
            return redirect('resume:home')

class AddProjectView(View):
    def get(self, request, pk,  *args, **kwargs):
        resume = Resume.objects.get(user=request.user, pk=pk)
        form = ProjectForm()
        context = {
            'form': form,
        }
        return render (self.request, 'resume/addproject.html', context)

    def post(self, request, pk, *args, **kwargs):
        try:
            resume = Resume.objects.get(user=request.user, pk=pk)
            form = ProjectForm(self.request.POST or None)
            if form.is_valid:
                body = form.save(commit=False)
                body.user = self.request.user
                body.resume = resume
                body.save()
                return redirect('resume:add_experience', pk=body.pk)
            else:
                return redirect('resume:home')

        except ObjectDoesNotExist:
            return redirect('resume:home')


class AddWorkView(View):
    def get(self, request, pk,  *args, **kwargs):
        resume = Resume.objects.get(user=request.user, pk=pk)
        form = WorkForm()
        context = {
            'form': form,
        }
        return render (self.request, 'resume/addwork.html', context)

    def post(self, request, pk, *args, **kwargs):
        try:
            resume = Resume.objects.get(user=request.user, pk=pk)
            form = WorkForm(self.request.POST or None)
            if form.is_valid:
                body = form.save(commit=False)
                body.user = self.request.user
                body.resume = resume
                body.save()
                return redirect('resume:add_responsibility', pk=body.pk)
            else:
                return redirect('resume:home')

        except ObjectDoesNotExist:
            return redirect('resume:home')

def experience(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = ExperienceForm(request.POST)
        if form.is_valid:
            body = form.save(commit=False)
            body.project = project
            body.user = request.user
            body.save()
            return redirect('resume:home')
        form = ExperienceForm()
    else:
        form = ExperienceForm()

    context = {
        'form': form,
        'project':project,
    }
    return render(request, 'resume/addexperience.html', context)


def responsibility(request, pk):
    work = get_object_or_404(Work, pk=pk)
    if request.method == "POST":
        form = ResponsibilityForm(request.POST)
        if form.is_valid:
            body = form.save(commit=False)
            body.work = work
            body.user = request.user
            body.save()
            return redirect('resume:home')
        form = ResponsibilityForm()
    else:
        form = ResponsibilityForm()

    context = {
        'form': form,
        'work': work,
    }
    return render(request, 'resume/addresponsibility.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = NewUSerForm(request.POST)
        if form.is_valid():
            user = form.save()
            Userprofile.objects.create(user=user)
            return redirect('resume:home')
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
    def post(self, *args, **kwargs):
        form = LoginForm(self.request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(self.request, user)
            return redirect ('resume:home')
        else:
            return redirect ('resume:login')

def logout(request):
    auth.logout(request)
    return redirect ('resume:home')


def user_edit(request, pk):
    d_user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = EditUserForm(request.POST, instance=d_user)
        if form.is_valid:
            user = form.save(commit=False)
            user.user = request.user
            user.save()
            return redirect('account:user_detail', pk=user.pk)
        form = EditUserForm()
    else:
        form = EditUserForm(instance=d_user)

    context = {
        'form': form
    }
    return render(request, 'registrations/user_edit.html', context)


def profile_edit(request):
    user_profile = get_object_or_404(Userprofile, user=request.user)
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=user_profile)
        if form.is_valid:
            user = form.save(commit=False)
            user.user = request.user
            user.created_date = timezone.now()
            user.save()
            return redirect('resume:home')
        form = EditProfileForm()
    else:
        form = EditProfileForm(instance=user_profile)

    context = {
        'form': form
    }
    return render(request, 'registrations/profile_edit.html', context)