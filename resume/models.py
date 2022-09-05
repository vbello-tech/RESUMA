from django.db import models
from django.utils import timezone
from django.shortcuts import reverse
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class Resume(models.Model):
    user = models.ForeignKey('auth.user', on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    resume_link = models.URLField(blank=True, null=True)

    def add_project(self):
        return reverse("resume:add_project", kwargs={
            'pk': self.pk,
        })

    def add_work(self):
        return reverse("resume:add_work", kwargs={
            'pk': self.pk,
        })

    def __str__(self):
        return self.name

class Project(models.Model):
    user = models.ForeignKey('auth.user', on_delete=models.CASCADE)
    resume = models.ForeignKey('Resume', related_name="resume", null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=250, blank=False, null=False)
    github = models.URLField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Experience(models.Model):
    project = models.ForeignKey('Project', related_name="project", on_delete=models.CASCADE)
    user = models.ForeignKey('auth.user', related_name="experience_gainer", on_delete=models.CASCADE)
    body = models.CharField(max_length=500, blank=False, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'EXPERIENCE "%s" GAINED FROM  project "%s"-(%s)' % (self.user, self.project.name, self.project.resume)


class Work(models.Model):
    user = models.ForeignKey('auth.user', on_delete=models.CASCADE)
    resume = models.ForeignKey('Resume', related_name="resume_work", null=True, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=300)
    company_description = models.CharField(max_length=250, blank=False, null=False)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.company_name


class Responsibility(models.Model):
    work = models.ForeignKey('Work', related_name="work", on_delete=models.CASCADE)
    user = models.ForeignKey('auth.user', related_name="responsibilty_owner", on_delete=models.CASCADE)
    body = models.CharField(max_length=500, blank=False, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'EXPERIENCE "%s" GAINED FROM  work "%s"-(%s)' % (self.user, self.work.company_name, self.work.resume)

class Userprofile(models.Model):
    user = models.OneToOneField('auth.user', on_delete=models.CASCADE)
    phone = PhoneNumberField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    portfolio = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    has_profile = models.BooleanField(default=False, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user}  profile"