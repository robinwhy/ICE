from django.conf.urls import url
from . import views

app_name = 'operation'

urlpatterns = [
    url(r'login_success/$', views.login_success, name='login_success')
]