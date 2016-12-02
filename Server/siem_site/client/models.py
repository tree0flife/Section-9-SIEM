from django.db import models
from django import forms

class Client(models.Model):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)