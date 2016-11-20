from django.db import models
from django import forms

class Member(models.Model):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=20)
    username = forms.EmailField(max_length=20)
    password = forms.EmailField(max_length=20)
