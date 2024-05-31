from django.db import models
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    birth_day = models.DateField()



def __str__(self):
        return self.user.username