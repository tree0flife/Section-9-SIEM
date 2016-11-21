from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.http import HttpResponse
from .forms import LoginForm

class LoginFormView(View):
    form_class = LoginForm
    template_name = 'login/login.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'login/homepage.html')

        return render(request, self.template_name, {'form': form})

