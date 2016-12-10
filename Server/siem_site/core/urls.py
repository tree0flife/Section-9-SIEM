from django.conf.urls import url
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='core.html'), name='core'),
    url(r'^bash_history_user/$', views.View_Bash_History_User.as_view(), name='bash_history_user'),
    url(r'^browser_history/$', views.View_Browser_History_User.as_view(), name='browser_history_user'),

]
