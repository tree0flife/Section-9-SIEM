from django.conf.urls import url
#from .views import view_bash_history_user
from . import  views
app_name = 'core'

urlpatterns = [
    url(r'^bash_history_user', views.view_bash_history_user.as_view(), name='bash_history_user'),
]
