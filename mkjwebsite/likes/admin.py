from django.contrib import admin
from .models import LikeCount, LikeRecord

# Register your models here.

@admin.register(LikeCount)
class LikeCountAdmin(admin.ModelAdmin):
    list_display = ('id', 'liked_cound', 'content_object')


@admin.register(LikeRecord)
class LikeRecord(admin.ModelAdmin):
    list_display = ('id', 'liked_time', 'user', 'content_object')

