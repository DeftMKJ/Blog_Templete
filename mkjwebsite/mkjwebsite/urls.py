"""mkjwebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', views.home, name='home'),
    re_path(r'^login/$', views.login, name='login'),
    re_path(r'^register/$', views.register, name='register'),
    re_path(r'^comment/', include('comment.urls', namespace='comment_module')),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    re_path(r'^blogs/', include('blogs.urls', namespace='blogs_module')),
]

# 该方法是临时测试用的，部署之前需要替换掉 TODO
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
