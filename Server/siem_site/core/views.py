from django.shortcuts import render
from django.views.generic import View

from .forms import *
from stats.methods.bash_history import *


class view_bash_history_user(View):
    form_class = Bash_History_User_Form
    template = 'test_graph.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']

        chart = bash_history_user(user)
        return render(request, template_name=self.template, context= {'chart': chart} )