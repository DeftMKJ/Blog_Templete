from django.shortcuts import render, redirect
from .models import Comment
from django.urls import reverse
from .forms import CommentForm
from django.http import JsonResponse


# Create your views here.


def comment_update(request):
    comment_form = CommentForm(request.POST, user=request.user)
    res = {}
    if comment_form.is_valid():
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']

        parent = comment_form.cleaned_data['parent']
        # 回复评论
        if not parent is None:
            comment.parent = parent
            # 如果父评论的顶级评论是空的，那么顶级就是parent 否则就是上一级的root
            comment.root = parent.root if not parent.root is None else parent
            comment.reply_to = parent.user
        comment.save()

        res['status'] = "SUCCESS"
        res['username'] = comment.user.username
        res['comment_time'] = comment.comment_time.timestamp()
        res['text'] = comment.text

        if not parent is None:
            res['reply_to'] = comment.reply_to.username
        else:
            res['reply_to'] = ''
        res['pk'] = comment.pk
        res['root_pk'] = comment.root.pk if not comment.root is None else ''

    else:
        res['status'] = "ERROR"
        res['message'] = list(comment_form.errors.values())[0][0]

    return JsonResponse(res)
