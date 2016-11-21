from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import MemberForm
from .models import Member

class MemberRegisterView(View):
    form_class = MemberForm
    template_name = 'register/register.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
    #
    #     if form.is_valid():
    #
    #     return render(request, self.template_name, {'form': form})
    #     I am Imad... and I like food.
