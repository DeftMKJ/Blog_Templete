from django.db import models
from django.contrib.auth.models import User


class Introduction(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='昵称')
    nick_name = models.CharField(max_length=20)

    def __str__(self):
        return "<%s for %s>" % (self.nick_name, self.user.username)
