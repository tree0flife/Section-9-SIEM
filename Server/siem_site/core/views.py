from django.shortcuts import render
from django.views.generic import View

from .forms import *
from .methods.bash_history import *


class View_Bash_History_Client(View):
    form_class = Bash_History_Client_Form
    template = 'bash_history_client.html'

    def get(self, request):
        form = self.form_class(None)
        context={
            'form': form
        }
        return render(request, self.template, context=context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            client = form.cleaned_data['client']
        #sets context
        #call stats app methods (convoluded)/should rename core to stats and move those methods here
        chart = bash_history_client(client)
        form = self.form_class(request.POST)
        context={
            'chart': chart,
            'form': form
        }
        return render(request, template_name=self.template, context=context)

class View_Browser_History_Client(View):
    def get (self,request):
        return 'memes'
    def post(self,request):
        return'memes'