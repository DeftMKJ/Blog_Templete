from django.urls import path, re_path
from . import views

app_name = 'blogs'

urlpatterns = [
    re_path(r'^$',views.blog_index, name='blog_index'),
    re_path(r'^detail/(\d+)/$',views.blog_details, name='blog_details'),
]