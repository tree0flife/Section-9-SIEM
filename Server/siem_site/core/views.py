from django.shortcuts import render
from django.views.generic import View

from .forms import *
from stats.methods.bash_history import *


class view_bash_history_user(View):
    form_class = Bash_History_User_Form
    template = 'bash_history_user.html'
    #template ='testgraph.html'

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
