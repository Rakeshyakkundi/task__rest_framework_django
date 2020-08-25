from django.forms import ModelForm
from .models import *
from django import forms
from django.core import validators
from django.contrib.auth.forms import UserCreationForm
from datetime import date
from datetime import datetime

class createuserform(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']