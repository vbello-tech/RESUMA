from django.db import models
from django.utils import timezone
from django.shortcuts import reverse
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class Userprofile(models.Model):
    user = models.OneToOneField('auth.user', on_delete=models.CASCADE)
    phone = PhoneNumberField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    experience_year = models.IntegerField(blank=True, null=True)
    portfolio = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    has_profile = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user}  profile"
