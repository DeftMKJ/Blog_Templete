from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment
from ..forms import CommentForm

register = template.Library()


# 需要通过{% load comment_tags %}导入 然后在使用里面的方法
# <li>评论：({% get_comment_count blog %})</li>
@register.simple_tag
def get_comment_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type, object_id=obj.pk).count()


@register.simple_tag
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return CommentForm(initial={'content_type': content_type.model, 'object_id': obj.pk, 'reply_comment_id': 0})


@register.simple_tag
def get_comment_lists(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(content_type=content_type, object_id=obj.pk, parent=None)
    return comments.order_by('-comment_time')



# 过滤器  ooo | add_xxx:1990  其中ooo作为value传入，1990作为arg传入
# @register.filter(name='add_xxx')
# def add_xxx(value, arg):
#     return "%sxxx%s" % (value, arg)
#
# <li>评论：({{ blog.get_read_num|add_xxx:1990 }})</li>
