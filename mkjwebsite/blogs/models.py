from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadNumExtension, ReadNumDetail
from django.contrib.contenttypes.fields import GenericRelation


class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name


class Blog(models.Model,ReadNumExtension):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    readDetails = GenericRelation(ReadNumDetail)  # 反向关联获取


    def __str__(self):
        return "<Blog:%s>" % self.title

    # 添加作用分页，主要需要数据库迁移
    class Meta:
        ordering = ['-create_time']
