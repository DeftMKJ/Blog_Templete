from django.shortcuts import render, get_object_or_404
from .models import Blog, BlogType
from django.core.paginator import Paginator
from django.conf import settings


def blog_datas_common(request, lists):
    paginator = Paginator(lists, settings.EACH_PAGE_NUMBERS)
    current_page_num = request.GET.get('page', '1')

    if not current_page_num.isdigit():
        print('非法数字')
        current_page_num = '1'
    if int(current_page_num) > paginator.num_pages:
        current_page_num = paginator.num_pages
    if int(current_page_num) < 1:
        current_page_num = '1'

    page_of_blogs = paginator.get_page(current_page_num)
    page_range = list(range(max(int(current_page_num) - 2, 1), int(current_page_num))) + \
                 list(range(int(current_page_num), min(int(current_page_num) + 2, paginator.num_pages) + 1))
    print(page_range)

    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')

    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context = {}
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blogTypes'] = BlogType.objects.all()
    context['blogDates'] = Blog.objects.dates('create_time', 'month', 'DESC')
    return context


# Create your views here.
def blog_index(request):
    blogs = Blog.objects.all()
    context = blog_datas_common(request, blogs)
    return render(request, 'blogs/blog_index.html', context)


def blog_types(request, blog_type):
    blogType = get_object_or_404(BlogType, pk=blog_type)
    blogs = Blog.objects.filter(blog_type=blogType)
    context = blog_datas_common(request, blogs)
    context['blog_type'] = blogType
    return render(request, 'blogs/blog_type_list.html', context)


def blog_dates(request, year, month):
    blogs = Blog.objects.filter(create_time__year=year, create_time__month=month)
    context = blog_datas_common(request, blogs)
    context['blog_title_with_date'] = "%s年%s月" % (year, month)
    return render(request, 'blogs/blog_dates.html', context)


def blog_details(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    pre_blog = Blog.objects.filter(create_time__gt=blog.create_time).last()
    next_blog = Blog.objects.filter(create_time__lt=blog.create_time).first()
    context = {}
    context['blog'] = blog
    context['previous_blog'] = pre_blog
    context['next_blog'] = next_blog
    return render(request, 'blogs/blog_detail.html', context)
