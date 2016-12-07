from django.shortcuts import render
from .forms import ClientForm
from django.views.generic import View

class View_Client(View):
    form_class = ClientForm
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

            return render(request, self.template_name, {'form': form})
