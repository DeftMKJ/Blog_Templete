from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

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



    def __str__(self):
        return self.text

    class Meta:
        ordering = ['comment_time']
