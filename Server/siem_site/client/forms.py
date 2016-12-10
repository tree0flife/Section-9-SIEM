from.models import Client
from django import forms

class Client_Form(forms.ModelForm):

    class Meta:
        model = Client
        fields = ['username', 'password', 'token']