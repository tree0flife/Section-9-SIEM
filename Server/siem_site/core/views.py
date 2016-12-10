from django.shortcuts import render
from django.views.generic import View

from .forms import *
from .methods.bash_history import *


class View_Bash_History_User(View):
    form_class = Bash_History_User_Form
    template = 'bash_history_user.html'

    def get(self, request):
        form = self.form_class(None)
        context={
            'form': form
        }
        return render(request, self.template, context=context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
        #sets context
        #call stats app methods (convoluded)/should rename core to stats and move those methods here
        chart = bash_history_user(user)
        form = self.form_class(request.POST)
        context={
            'chart': chart,
            'form': form
        }
        return render(request, template_name=self.template, context=context)

class View_Browser_History_User(View):
    def get (self,request):
        return 'memes'
    def post(self,request):
        return'memes'