from django.shortcuts import render,redirect
from .forms import Client_Form,Client_Form_Delete
from .models import Client
from django.views.generic import View

class View_Client_Add(View):
    form_class = Client_Form
    template_name = 'client_add.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            token = form.cleaned_data['token']
            form.save()
            form = self.form_class(None)
            context = {
                'form': form
            }
            return render(request, self.template_name, context=context)

class View_Client_List(View):
    template = 'client_list.html'

    def get(self,request):
        client_list = Client.objects.all()

        context={
            'client_list': client_list
        }
        return  render(request,self.template,context=context)

#delete_client
class View_Client_Delete(View):
    template = 'client_delete.html'
    form_class = Client_Form_Delete
    def get(self, request):
        form = self.form_class(None)
        context={'form': form}
        return render(request, template_name=self.template, context=context)

    def post(self,request):

        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            Client.objects.filter(username__contains=username).delete()
        return redirect('client_list')
