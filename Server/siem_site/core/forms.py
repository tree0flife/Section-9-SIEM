from django import forms

class Bash_History_User_Form(forms.Form):
    user = forms.CharField(label='user', max_length=30)