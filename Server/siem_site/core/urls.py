from django.conf.urls import url
from .views import view_bash_history_user
app_name = 'core'

urlpatterns = [
    url(r'^test', view_bash_history_user, name='test_graph')
]
