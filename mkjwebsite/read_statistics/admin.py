from django.contrib import admin
from .models import ReadNum, ReadNumDetail

# Register your models here.

@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('pk','read_num','content_object')


@admin.register(ReadNumDetail)
class ReadNumDetailAdmin(admin.ModelAdmin):
    list_display = ('pk','read_date','read_num','content_object')