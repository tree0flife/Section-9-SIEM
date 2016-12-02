from django.shortcuts import render, redirect
from .forms import ClientForm
from django.views.generic import View


class ClientView(View):
    form_class = ClientForm
    template_name = 'client.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            # user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            return redirect("{% url 'index' %}")
