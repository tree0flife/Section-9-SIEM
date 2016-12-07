"""siem_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

#from django.contrib.auth import views as auth_views
#from django.contrib.auth import views
from django.views.generic.base import TemplateView



urlpatterns = [

    url(r'^admin/', admin.site.urls),

    url(r'^$', TemplateView.as_view(template_name='homepage.html'), name='index'),
    url(r'^about_us', TemplateView.as_view(template_name ='about_us.html'), name='about_us'),
    url(r'contact_us', TemplateView.as_view(template_name ='contact_us.html'), name='contact_us'),
    #url(r'^register/', include('register.urls'), name='register'),
    #url(r'^$', include('auth_views.login')),

    url(r'^', include ('django.contrib.auth.urls')),
    #url(r'^forgot/$',auth_views.password_reset),
    #url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^accounts/', include('registration.backends.hmac.urls')),

    url(r'^core/', include('core.urls')),
]
