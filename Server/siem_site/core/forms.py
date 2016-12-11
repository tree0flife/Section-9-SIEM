from django import forms

class Client_Request_Form(forms.Form):
    client = forms.CharField(label='user', max_length=30)