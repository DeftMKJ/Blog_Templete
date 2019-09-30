from django.urls import re_path
from . import views

app_name = 'user'

urlpatterns = [
    re_path(r'^login_modal/$', views.login_modal, name='login_modal'),
    re_path(r'^login/$', views.login, name='login'),
    re_path(r'^register/$', views.register, name='register'),
    re_path(r'^logout/$', views.logout, name='logout'),
    re_path(r'^user_info/$', views.user_info, name='user_info'),
    re_path(r'^change_nickname/$', views.change_nick_name, name='change_nickname'),
]
