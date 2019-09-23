from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from django.urls import reverse

# Create your views here.


def comment_update(request):

    print('测试')
    print(request.POST.get('object_id', ''))
    user = request.user
    text = request.POST.get('comment_text', '')
    object_id = int(request.POST.get('object_id', ''))
    content_type = request.POST.get('content_type', '')

    comment_cls =  ContentType.objects.get(model=content_type).model_class()
    comment_obj = comment_cls.objects.get(pk=object_id)

    comment = Comment()

    comment.content_object = comment_obj
    comment.text = text
    comment.user = user
    comment.save()

    refer = request.META.get('HTTP_REFERER', reverse('home'))
    return redirect(refer)


