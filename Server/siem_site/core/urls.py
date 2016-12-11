from django.conf.urls import url
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='core.html'), name='core'),
    url(r'^bash_history_client/$', views.View_Bash_History_Client.as_view(), name='bash_history_client'),
    url(r'^browser_history_client/$', views.View_Browser_History_Client.as_view(), name='browser_history_client'),
    url(r'^download/$', views.View_Download_Client, name='browser_history_client'),
]
