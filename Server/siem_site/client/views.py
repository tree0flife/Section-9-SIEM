from django.shortcuts import render
from .forms import Client_Form
from django.views.generic import View

from .models import Client

class View_Client(View):
    form_class = Client_Form
    template_name = 'client.html'

    def get(self, request):

        form = self.form_class(None)
        #@TODO: make method here to query clients
        #@TODO: select all into a list and print through it all.
        #query = Client.objects.All




        #request.user  HttpRequest.user #to not see ALL credentials
        context={
            'form': form
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            username.save()
            password.save()

            context={
                'form': form
            }

            #@TODO SUBMIT, RESET, GROWING LIST , ALERT WHEN MODIFIYING THINGS
            return render(request, self.template_name,context=context )

class View_Client_Add(View):
    form_class = Client_Form
    template_name = 'client.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            #@TODO SUBMIT, RESET, GROWING LIST
            return render(request, self.template_name, {'form': form})
