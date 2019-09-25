from django.shortcuts import render, redirect
from .models import Comment
from django.urls import reverse
from .forms import CommentForm

# Create your views here.


def comment_update(request):
    refer = request.META.get('HTTP_REFERER', reverse('home'))
    comment_form = CommentForm(request.POST, user=request.user)
    if comment_form.is_valid():
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']
        comment.save()
        return redirect(refer)
    else:
        pass


