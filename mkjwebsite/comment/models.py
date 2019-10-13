import threading
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


# TODO 网站访问量大了用Celery来异步任务处理
class SendEmail(threading.Thread):
    def __init__(self, subject, text, email, fail_silently=False):
        self.subject = subject
        self.text = text
        self.email = email
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)


    def run(self):
        send_mail(
            self.subject,
            '',
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=self.fail_silently,
            html_message=self.text,
        )


# Create your models here.

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # 评论内容
    text = models.TextField()
    # 评论时间
    comment_time = models.DateTimeField(auto_now=True)
    # 评论的人
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)

    # 评论上一级评论的评论的人
    reply_to = models.ForeignKey(User, related_name='replies', null=True, on_delete=models.CASCADE)
    # 评论哪个评论，评论的爸爸 一级评论没有爸爸
    parent = models.ForeignKey('self', related_name='parent_comment', null=True, on_delete=models.CASCADE)
    # 顶级评论
    root = models.ForeignKey('self', related_name='root_comment', null=True, on_delete=models.CASCADE)


    def submit_comment(self):
        if self.parent is None:
            subjuect = '有人评论你博客'
            email = self.content_object.get_email()
        else:
            subjuect = '有人回复你的评论'
            email = self.reply_to.email
        if email != '':
            context = {}
            context['text'] = self.text
            context['url'] = self.content_object.get_url()
            text = render_to_string('comment/send_email.html', context)
            se =  SendEmail(subjuect, text, email)
            se.start()


    def __str__(self):
        if self.parent is None:
            return '顶级类型评论---%s' % self.text
        else:
            return '回复类型评论---%s' % self.text

    class Meta:
        ordering = ['comment_time']
