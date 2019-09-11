from django.shortcuts import render, get_object_or_404
from .models import Blog, BlogType


# Create your views here.
def blog_index(request):
    context = {}
    context['blogs'] = Blog.objects.all()
    return render(request, 'blogs/blog_index.html', context)

def blog_types(request, blog_type):
    context = {}
    blogType =  get_object_or_404(BlogType, pk=blog_type)
    context['blogs'] = Blog.objects.filter(blog_type=blogType)
    context['blog_type'] = blogType
    return render(request, 'blogs/blog_type_list.html', context)


def blog_details(request, blog_pk):
    context = {}
    context['blog'] = get_object_or_404(Blog, pk=blog_pk)
    return render(request, 'blogs/blog_detail.html', context)
