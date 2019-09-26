from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget
from .models import Comment


class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)

    # error_messages 错误的时候自定义抛出
    text = forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'),
                           error_messages={'required': '评论内容不能为空'})

    # 评论嵌套用  attrs的id用来js调用 对应评论的主键值 reply_comment_id js赋值用
    reply_comment_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id':'reply_comment_id'}))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(CommentForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户未登录')

        model = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']

        try:
            comment_cls = ContentType.objects.get(model=model).model_class()
            comment_obj = comment_cls.objects.get(pk=object_id)
            self.cleaned_data['content_object'] = comment_obj
        except ObjectDoesNotExist:
            raise forms.ValidationError('评论对象不存在')
        return self.cleaned_data

    # hook 回复评论的id 判断是否是顶级评论还是回复
    def clean_reply_comment_id(self):
        reply_comment =  self.cleaned_data['reply_comment_id']
        if reply_comment < 0:
            raise forms.ValidationError('回复出错')
        elif reply_comment == 0:
            # 顶级评论
            self.cleaned_data['parent'] = None
        elif Comment.objects.filter(pk=reply_comment).exists():
            # 回复
            self.cleaned_data['parent'] = Comment.objects.get(pk=reply_comment)
        else:
            raise forms.ValidationError('回复出错')
        return reply_comment

