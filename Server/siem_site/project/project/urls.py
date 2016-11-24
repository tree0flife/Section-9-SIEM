from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/', include('register.urls'), name='register'),
    url(r'^$', TemplateView.as_view(template_name='homepage.html'), name='homepage'),
    url(r'^login/$', views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', views.logout, {'template_name': 'logout.html'}, name='logout'),
]
