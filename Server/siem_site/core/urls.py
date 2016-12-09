from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^bash_history_user/$', views.view_bash_history_user.as_view(), name='bash_history_user'),
]
