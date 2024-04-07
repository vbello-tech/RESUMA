from django.db import models
from django.utils import timezone
from django.shortcuts import reverse
from phonenumber_field.modelfields import PhoneNumberField
import random, string
from ckeditor.fields import RichTextField


# Create your models here.


def create_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


Type_chioce = (
    ('LANGUAGE', 'LANGUAGE'),
    ('DATABASE', 'DATABASE'),
    ('FRAMEWORK', 'FRAMEWORK'),
    ('SOFTWARE', 'SOFTWARE'),
    ('CLOUD_PLATFORM', 'CLOUD_PLATFORM'),
    ('PARADIGM', 'PARADIGM'),
)


class Tech(models.Model):
    name = models.CharField(max_length=150, unique=True)
    type = models.CharField(max_length=200, choices=Type_chioce, blank=True, null=True)

    def __str__(self):
        return self.name


class Resume(models.Model):
    user = models.ForeignKey('auth.user', on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    resume_link = models.URLField(blank=True, null=True)
    skills = models.ManyToManyField("Tech", related_name="techskill", blank=True)
    slug = models.SlugField(default=create_code())

    def complete(self):
        return reverse("resume:complete_resume", kwargs={
            'pk': self.pk,
        })

    def add_project(self):
        return reverse("resume:add_project", kwargs={
            'pk': self.pk,
        })

    def add_work(self):
        return reverse("resume:add_work", kwargs={
            'pk': self.pk,
        })

    def add_education(self):
        return reverse("resume:add_education", kwargs={
            'pk': self.pk,
        })

    def add_skills(self):
        return reverse("resume:add_skills", kwargs={
            'pk': self.pk,
        })

    def get_preview(self):
        return reverse("resume:preview_resume", kwargs={
            'pk': self.pk,
        })

    def get_resume(self):
        return reverse("resume:resume", kwargs={
            'slug': self.slug,
            'name': self.name,
        })

    def __str__(self):
        return self.name


Field_chioce = (
    ('BSC SCIENCE', 'BSC SCIENCE'),
    ('BSC ENGINEERING', 'BSC ENGINEERING'),
    ('BSC FINANCE', 'BSC FINANCE'),
    ('BSC ECONOMICS AND BUSINESS', 'BSC ECONOMICS AND BUSINESS'),
    ('BSC APPLIED SCIENCES', 'BSC APPLIED SCIENCES'),
    ('BOOTCAMP', 'BOOTCAMP'),
    ('BSC LAW', 'BSC LAW'),
)


class Education(models.Model):
    user = models.ForeignKey('auth.user', on_delete=models.CASCADE)
    resume = models.ForeignKey('Resume', related_name="resume_edu", null=True, on_delete=models.CASCADE)
    school_name = models.CharField(max_length=300, blank=True, null=True)
    location = models.CharField(max_length=300, blank=True, null=True)
    field = models.CharField(max_length=300, choices=Field_chioce, blank=True, null=True)
    course = models.CharField(max_length=300, blank=True, null=True)
    enrollment_date = models.DateField(blank=True, null=True)
    graduation_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.school_name


class Project(models.Model):
    user = models.ForeignKey('auth.user', on_delete=models.CASCADE)
    resume = models.ForeignKey('Resume', related_name="resume", null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=400, blank=False, null=False)
    github = models.URLField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Work(models.Model):
    user = models.ForeignKey('auth.user', on_delete=models.CASCADE)
    resume = models.ForeignKey('Resume', related_name="resume_work", null=True, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=300)
    role = models.CharField(max_length=300, blank=True, null=True)
    company_description = RichTextField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.company_name
