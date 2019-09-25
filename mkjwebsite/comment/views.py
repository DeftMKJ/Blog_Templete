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
        comment.save()
        res['status'] = "SUCCESS"
        res['username'] = comment.user.username
        res['comment_time'] = comment.comment_time.strftime("%Y:%m:%d %H:%M:%S")
        res['text'] = comment.text

    else:
        res['status'] = "ERROR"
        res['message'] = list(comment_form.errors.values())[0][0]

    return JsonResponse(res)
