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
    re_path(r'^bind_email/$', views.bind_email, name='bind_email'),
    re_path(r'^send_email_code/$', views.send_email_code, name='send_email_code'),
    re_path(r'^change_password/$', views.change_password, name='change_password'),
    re_path(r'^forget_password/$', views.forget_password, name='forget_password'),
]
