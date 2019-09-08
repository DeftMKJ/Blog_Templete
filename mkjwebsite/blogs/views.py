from django.shortcuts import render, get_object_or_404
from .models import Blog, BlogType


# Create your views here.
def blog_index(request):
    context = {}
    context['blogs'] = Blog.objects.all()
    return render(request, 'blogs/blog_index.html', context)


def blog_details(request, blog_pk):
    context = {}
    context['blog'] = get_object_or_404(Blog, pk=blog_pk)
    return render(request, 'blogs/blog_detail.html', context)
