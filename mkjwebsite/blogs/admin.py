from django.contrib import admin
from .models import BlogType, Blog


@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('type_name',)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id','title','create_time','last_update_time','author','blog_type')
    ordering = ('-create_time',)
