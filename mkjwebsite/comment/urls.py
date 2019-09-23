from django.urls import re_path
from . import views

app_name = 'comment'

urlpatterns = [
    re_path(r'^update_comments/$', views.comment_update, name='comment_update'),
]
