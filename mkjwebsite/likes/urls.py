from django.urls import re_path
from . import views

app_name = 'likes'

urlpatterns = [
    re_path(r'^update_likes/$', views.likes_update, name='likes_update'),
]
