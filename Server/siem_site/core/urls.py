from django.conf.urls import url
from .views import view_bash_history_user
app_name = 'core'

urlpatterns = [
    url(r'^view_bash_history_user/$', view_bash_history_user.as_view(), name='view_bash_history_user'),
]
