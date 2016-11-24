from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.MemberFormView.as_view(), name='MemberFormView'),
]
