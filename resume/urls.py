from django.urls import path
from .views import *
from django.urls import path, reverse_lazy
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetCompleteView,
)

app_name ="resume"

urlpatterns =[
    path('', home, name="home"),
    path('add-resume/', AddResumeView.as_view(), name="add_resume"),
    path('resume/user/resume/', user_resume, name="user_resume"),
    path('add-resume/add-project/<int:pk>', AddProjectView.as_view(), name="add_project"),
    path('add-resume/add-work/<int:pk>', AddWorkView.as_view(), name="add_work"),
    path('add-resume/add-education/<int:pk>', AddEducationView.as_view(), name="add_education"),
    path('add-resume/add-skills/<int:pk>', AddSkillsView.as_view(), name="add_skills"),
    path('resume/<int:pk>/generate-pdf/', GeneratePdf.as_view(), name="generate_pdf"),
    path('resume/<int:pk>/generate-link/', generate_link, name="generate_link"),
    path('resume/<int:pk>/preview/', ResumePreviewView.as_view(), name="preview_resume"),
    path('resume/<str:slug>/', ResumeView.as_view(), name="resume"),
]