from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import LoginForm

class MemberLoginView(View):
    form_class = LoginForm
    template_name = 'login/login.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            form = self.form_class(request.POST)

        return render(request, self.template_name, {'form': form})