from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.views.generic import TemplateView, DetailView, View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
import urllib.parse
from django.conf import settings
from accounts.models import Userprofile
from django.contrib import messages

# Create your vieWS HERE
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
                    project = Project.objects.create(
                        resume = resume,
                        user=request.user,
                        name=name,
                        description=description,
                        github=github,
                        link=link,
                    )
                    return redirect(resume.add_project())
                else:
                    return redirect('resume:home')
            else:
                return redirect('resume:login')
        except ObjectDoesNotExist:
            return redirect('resume:home')


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
                return redirect(resume.add_work())
            else:
                return redirect('resume:home')

        except ObjectDoesNotExist:
            return redirect('resume:home')

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
        if form.is_valid():
            print(resume)
            school_name = form.cleaned_data.get('school_name')
            print(school_name)
            location = form.cleaned_data.get('location')
            print(location)
            field = form.cleaned_data.get('field')
            print(field)
            course = form.cleaned_data.get('course')
            print(course)
            enrollment_date = form.cleaned_data.get('enrollment_date')
            graduation_date = form.cleaned_data.get('graduation_date')
            print(enrollment_date, graduation_date)
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
    def get(self, request, slug,  *args, **kwargs):
        resume = Resume.objects.get(slug=slug)
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


