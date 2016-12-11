from django.shortcuts import render
from django.views.generic import View
from django.http import StreamingHttpResponse
from .forms import Client_Request_Form

from .methods.bash_history import bash_history_client
from .methods.pcap import outbound_ip_client


class View_Bash_History_Client(View):
    form_class = Client_Request_Form
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
        chart = bash_history_client(client)
        form = self.form_class(request.POST)
        context={
            'chart': chart,
            'form': form
        }
        return render(request, template_name=self.template, context=context)

class View_Outbound_IP_Client(View):
    template ='outbound_ip_client.html'
    form_class = Client_Request_Form
    def get (self,request):
        form = self.form_class(None)
        context={'form': form}
        return render(request, self.template, context=context)

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            client = form.cleaned_data['client']
        chart = outbound_ip_client(client)
        form = self.form_class(request.POST)
        context = {
            'chart': chart,
            'form': form
        }
        return render(request, template_name=self.template, context=context)


def View_Download_Client(request):
    path_to_file = 'media/siem9-client-1.0.0.zip'
    zip_file = open(path_to_file, 'rb')
    response = StreamingHttpResponse(zip_file, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="%s"' % 'siem9-client-1.0.0.zip'
    return response

