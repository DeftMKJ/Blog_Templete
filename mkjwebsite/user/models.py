from django.db import models
from django.contrib.auth.models import User


class Introduction(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='昵称')
    nick_name = models.CharField(max_length=20)

    def __str__(self):
        return "<%s for %s>" % (self.nick_name, self.user.username)


def get_nickname(self):
    if Introduction.objects.filter(user=self).exists():
        introduction = Introduction.objects.get(user=self)
        return introduction.nick_name
    else:
        return '未设置'


def get_nickname_or_username(self):
    if Introduction.objects.filter(user=self).exists():
        introduction = Introduction.objects.get(user=self)
        return introduction.nick_name
    else:
        return self.username


def has_nickname(self):
    return Introduction.objects.filter(user=self).exists()


User.get_nickname = get_nickname
User.get_nickname_or_username = get_nickname_or_username
User.has_nickname = has_nickname
