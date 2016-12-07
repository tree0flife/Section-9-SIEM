from django.contrib.auth.models import User
from django import forms

class Client_Form(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password']