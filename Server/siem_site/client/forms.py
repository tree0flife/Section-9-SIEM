from.models import Client
from django import forms

class Client_Form(forms.ModelForm):

    class Meta:
        model = Client
        fields = ['username', 'password', 'token']
class Client_Form_Delete(forms.ModelForm):

        class Meta:
            model =Client
            fields =['username']