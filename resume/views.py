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
import urllib.parse
from django.conf import settings

# Create your vie
#PDF
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
from xhtml2pdf import pisa
import os

#function to convert html to pdf
def html_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

#RENDER RESUME TO PDF
class GeneratePdf(View, LoginRequiredMixin):
    def get(self, request, pk, *args, **kwargs):
        mainuser = User.objects.get(username=request.user)
        userprofile = Userprofile.objects.get(user=request.user)
        resume = Resume.objects.get(user=self.request.user, pk=pk)
        project = Project.objects.filter(user=request.user, resume=resume)
        work = Work.objects.filter(user=request.user, resume=resume)
        education = Education.objects.filter(user=request.user, resume=resume)
        open('templates/resume/resumepdf.html', "w").write(render_to_string('resume/resume.html',
                                                                            {
            'user':mainuser,
            'userp':userprofile,
            'resume':resume,
            'projects':project,
            'works':work,
            'education':education,
        }))
        pdf = html_to_pdf('resume/resumepdf.html')
        #return HttpResponse(pdf, content_type='application/pdf')


        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "%s %s %s RESUME" % (self.request.user.last_name, self.request.user.first_name, resume.name)
            #content = "inline; filename=%s" % (filename)
            content = "attachment; filename=%s.pdf" %(filename)
            response['Content-disposition']=content
            return response
        return HttpResponse("Not Found")


#HOMEPAGE
def home(request):
    context ={
        'user':request.user
    }
    return render(request, 'home.html', context)

#HOMEPAGE
@login_required
def user_resume(request):
    resume = Resume.objects.filter(user=request.user)
    context ={
        'user':request.user,
        'resumes':resume,
    }
    return render(request, 'resume/user_resume.html', context)

#CREATE REUSUME
class AddResumeView(View, LoginRequiredMixin):
    def get(self, *args, **kwargs):
        form = ResumeForm()
        context = {
            'form': form,
        }
        return render (self.request, 'resume/addresume.html', context)

    def post(self, *args, **kwargs):
        try:
            form = ResumeForm(self.request.POST or None)
            if self.request.user.is_authenticated:
                if form.is_valid():
                    resume = form.save(commit=False)
                    resume.user = self.request.user
                    resume.save()
                    return redirect(resume.add_project())
                else:
                    return redirect('resume:home')
            else:
                return redirect('resume:login')

        except ObjectDoesNotExist:
            return redirect('resume:home')

#ADD PROJECT TO RESUME
class AddProjectView(View, LoginRequiredMixin):
    def get(self, request, pk,  *args, **kwargs):
        resume = Resume.objects.get(user=request.user, pk=pk)
        form = ProjectForm()
        context = {
            'resume':resume,
            'form': form,
        }
        return render (self.request, 'resume/addproject.html', context)

    def post(self, request, pk, *args, **kwargs):
        try:
            if self.request.user.is_authenticated:
                resume = Resume.objects.get(user=request.user, pk=pk)
                form = ProjectForm(self.request.POST or None)
                if form.is_valid():
                    name = form.cleaned_data.get('name')
                    description = form.cleaned_data.get('description')
                    github = form.cleaned_data.get('github')
                    link = form.cleaned_data.get('link')
                    experience = form.cleaned_data.get('experience')
                    project = Project.objects.create(
                        resume = resume,
                        user=request.user,
                        name=name,
                        description=description,
                        github=github,
                        link=link,
                    )
                    exp = Experience.objects.create(
                        project=project,
                        user=request.user,
                        body=experience
                    )
                    return redirect(resume.add_project())
                else:
                    return redirect('resume:home')
            else:
                return redirect('resume:login')
        except ObjectDoesNotExist:
            return redirect('resume:home')


#ADD EXPERIENCED YOU GAINED WHILE WORKING ON PROJECT
@login_required
def experience(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = ExperienceForm(request.POST)
        if form.is_valid:
            body = form.save(commit=False)
            body.project = project
            body.user = request.user
            body.save()
            return redirect('resume:preview_resume', pk=project.resume.pk)
        form = ExperienceForm()
    else:
        form = ExperienceForm()

    context = {
        'form': form,
        'project':project,
    }
    return render(request, 'resume/addexperience.html', context)


#ADD WORK EXPERIENCE
class AddWorkView(View, LoginRequiredMixin):
    def get(self, request, pk,  *args, **kwargs):
        resume = Resume.objects.get(user=request.user, pk=pk)
        form = WorkForm()
        context = {
            'form': form,
            'resume':resume,
        }
        return render (self.request, 'resume/addwork.html', context)

    def post(self, request, pk, *args, **kwargs):
        try:
            resume = Resume.objects.get(user=request.user, pk=pk)
            form = WorkForm(self.request.POST or None)
            if form.is_valid():
                company_name = form.cleaned_data.get('company_name')
                company_description = form.cleaned_data.get('company_description')
                role = form.cleaned_data.get('role')
                responsibility = form.cleaned_data.get('responsibility')
                start_date = form.cleaned_data.get('start_date')
                end_date = form.cleaned_data.get('end_date')
                work = Work.objects.create(
                    resume=resume,
                    user=request.user,
                    company_name=company_name,
                    company_description=company_description,
                    role=role,
                    start_date=start_date,
                    end_date=end_date,
                )
                res = Responsibility.objects.create(
                    work=work,
                    user=request.user,
                    body=responsibility
                )
                return redirect(resume.add_work())
            else:
                return redirect('resume:home')

        except ObjectDoesNotExist:
            return redirect('resume:home')

#ADD EXPERIENCE YOU GAINED AND YOUR RESPONSIBILITY ON THE JOB
@login_required
def responsibility(request, pk):
    work = get_object_or_404(Work, pk=pk)
    if request.method == "POST":
        form = ResponsibilityForm(request.POST)
        if form.is_valid:
            body = form.save(commit=False)
            body.work = work
            body.user = request.user
            body.save()
            return redirect('resume:preview_resume', pk=work.resume.pk)
        form = ResponsibilityForm()
    else:
        form = ResponsibilityForm()

    context = {
        'form': form,
        'work': work,
    }
    return render(request, 'resume/addresponsibility.html', context)


#ADD EDUCATION HISTORY
class AddEducationView(View, LoginRequiredMixin):
    def get(self, request, pk,  *args, **kwargs):
        resume = Resume.objects.get(user=request.user, pk=pk)
        form = EducationForm()
        context = {
            'form': form,
            'resume':resume,
        }
        return render (self.request, 'resume/addeducation.html', context)

    def post(self, request, pk, *args, **kwargs):
        resume = Resume.objects.get(user=request.user, pk=pk)
        form = EducationForm(self.request.POST or None)
        if request.method == "POST" and form.is_valid():
            #if form.is_valid():
            print(resume)
            school_name = form.cleaned_data.get('school_name')
            location = form.cleaned_data.get('location')
            field = form.cleaned_data.get('field')
            course = form.cleaned_data.get('course')
            enrollment_date = form.cleaned_data.get('enrollment_date')
            graduation_date = form.cleaned_data.get('graduation_date')
            education = Education.objects.create(
                resume=resume,
                user=request.user,
                school_name=school_name,
                location=location,
                field=field,
                course=course,
                enrollment_date=enrollment_date,
                graduation_date=graduation_date,
            )
            print(school_name)
            return redirect(resume.add_education())
        else:
            return redirect('resume:home')



# ADD EDUCATION HISTORY
class AddSkillsView(View, LoginRequiredMixin):
    def get(self, request, pk, *args, **kwargs):
        resume = Resume.objects.get(user=request.user, pk=pk)
        form = SkillsForm()
        context = {
            'form': form,
            'resume': resume,
        }
        return render(self.request, 'resume/addskills.html', context)

    def post(self, request, pk, *args, **kwargs):
        try:
            resume = Resume.objects.get(user=request.user, pk=pk)
            form = SkillsForm(self.request.POST or None)
            if form.is_valid():
                tech = form.cleaned_data.get('tech')
                resume.skills.set(tech),
                return redirect(resume.get_preview())
            else:
                return redirect('resume:home')

        except ObjectDoesNotExist:
            return redirect('resume:home')


#PREVIEW RESUME
class ResumePreviewView(View, LoginRequiredMixin):
    def get(self, request, pk,  *args, **kwargs):
        mainuser = User.objects.get(username=request.user)
        userprofile = Userprofile.objects.get(user=request.user)
        resume = Resume.objects.get(user=self.request.user, pk=pk)
        project = Project.objects.filter(user=request.user, resume=resume)
        work = Work.objects.filter(user=request.user, resume=resume)
        education = Education.objects.filter(user=request.user, resume=resume)
        context =  {
            'user':mainuser,
            'userp':userprofile,
            'resume':resume,
            'projects':project,
            'works':work,
            'education':education,
        }
        return render (self.request, 'resume/resume_review.html', context)

#GENERATE RESUME LINK
@login_required
def generate_link(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    if resume.resume_link:
        return redirect(resume.get_preview())
    else:
        r_code = resume.slug
        query = urllib.parse.quote(r_code)
        if settings.DEBUG:
            url = 'http://127.0.0.1:8000/resume/'+query
        else:
            url = 'https://resumebuilder.fly.dev/resume/'+query
        resume.resume_link = url
        resume.save()
        return redirect(resume.get_preview())


#PREVIEW RESUME
class ResumeView(View):
    def get(self, request, user, name, slug,  *args, **kwargs):
        resume = Resume.objects.get(slug=slug, name=name)
        mainuser = User.objects.get(username=resume.user.username)
        userprofile = Userprofile.objects.get(user=resume.user)
        project = Project.objects.filter(resume=resume)
        work = Work.objects.filter(resume=resume)
        education = Education.objects.filter(resume=resume)
        context =  {
            'user':mainuser,
            'userp':userprofile,
            'resume':resume,
            'projects':project,
            'works':work,
            'education':education,
        }
        return render (self.request, 'resume/resumeview.html', context)

# AUTHORIZATION
def signup_view(request):
    if request.method == 'POST':
        form = NewUSerForm(request.POST)
        if form.is_valid():
            user = form.save()
            Userprofile.objects.create(user=user)
            return redirect('resume:create_profile')
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
            user_p = Userprofile.objects.get(user=user)
            if user_p.has_profile:
                return redirect ('resume:home')
            else:
                return redirect('resume:create_profile')
        else:
            return redirect ('resume:login')

def logout(request):
    auth.logout(request)
    return redirect ('resume:home')

@login_required
def user_edit(request, pk):
    d_user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = EditUserForm(request.POST, instance=d_user)
        if form.is_valid:
            user = form.save(commit=False)
            user.user = request.user
            user.save()
            return redirect('resume:user_detail', pk=user.pk)
        form = EditUserForm()
    else:
        form = EditUserForm(instance=d_user)

    context = {
        'form': form
    }
    return render(request, 'registrations/user_edit.html', context)


# CHECK OUT VIEW
class CreateProfileView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            if self.request.user.is_authenticated:
                userprofile = Userprofile.objects.get(user=self.request.user)
            else:
                return redirect('resume:login')
        except ObjectDoesNotExist:
            return redirect('resume:sign_up')
        form = ProfileForm()
        context = {
            'form': form,
            'userprofile':userprofile
        }
        return render (self.request, 'resume/createprofile.html', context)

    def post(self, *args, **kwargs):
        try:
            userprofile = Userprofile.objects.get(user=self.request.user)
            if userprofile.has_profile:
                return redirect('resume:home')
            else:
                form = ProfileForm(self.request.POST or None)
                if form.is_valid():
                    bio = form.cleaned_data.get('bio')
                    phone = form.cleaned_data.get('phone')
                    github = form.cleaned_data.get('github')
                    portfolio = form.cleaned_data.get('portfolio')
                    linkedin = form.cleaned_data.get('linkedin')
                    userprofile.bio = bio
                    userprofile.phone = phone
                    userprofile.github = github
                    userprofile.portfolio = portfolio
                    userprofile.linkedin = linkedin
                    userprofile.has_profile = True
                    userprofile.save()
                    return redirect('resume:user_detail')
                else:
                    return redirect('resume:sign_up')

        except ObjectDoesNotExist:
            return redirect('resume:sign_up')

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
            return redirect('resume:user_detail', pk=request.user.pk)
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
            return redirect('resume:user_detail')
    else:
        form = PasswordChangeForm(data=request.POST, user=request.user)

    context = {
        'form': form
    }
    return render(request, 'registrations/change_password.html', context)



def handler404(request, exception):
    context = {'word':"<h1>PAGE NOT FOUND!! ARE YOU SURE YOU ARE NAVIGATING TO THE RIGHT PAGE?</h1>"}
    response = render(request, "404.html", context)
    response.status_code = 404
    return response


def handler500(request):
    context = {'word':"<h1>OOPS !!! <br> SEVER ERROR!!! <br> </h1>"}
    response = render(request, "500.html", context)
    response.status_code = 500
    return response

