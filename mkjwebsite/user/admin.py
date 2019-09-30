from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Introduction


class IntroductionInline(admin.StackedInline):
    model = Introduction
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (IntroductionInline,)
    list_display = ('username', 'nickname', 'email', 'is_staff', 'is_active', 'is_superuser')

    # <class 'django.contrib.auth.models.User'>  obj
    def nickname(self, obj):
        return obj.introduction.nick_name

    nickname.short_description = '昵称'


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Introduction)
class IntroductionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'nick_name')
