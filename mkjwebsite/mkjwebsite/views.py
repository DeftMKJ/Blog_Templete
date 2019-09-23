from django.shortcuts import render, get_object_or_404, redirect
from read_statistics.utils import get_seven_days_read_statistics, get_hot_today_read_statistics, \
    get_hot_yestoday_read_statistics
from blogs.models import Blog
from django.contrib.contenttypes.models import ContentType
import datetime
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache
from django.contrib import auth
from django.urls import reverse
from .forms import LoginForm
from django.contrib import auth
from django import forms


def get_seven_hots_read_statistics():
    today = timezone.now().date()
    seven_days = today - datetime.timedelta(days=7)
    results = Blog.objects \
        .filter(readDetails__read_date__lt=today, readDetails__read_date__gte=seven_days) \
        .values('id', 'title') \
        .annotate(read_num_sum=Sum('readDetails__read_num')) \
        .order_by("-read_num_sum")
    print('七天数据:%s' % results)
    return results[:7]


def home(request):
    contentType = ContentType.objects.get_for_model(Blog)
    context = {}
    dates, counts = get_seven_days_read_statistics(contentType)

    hot_7_days_blogs = cache.get("hot_7_days_blogs")
    if hot_7_days_blogs is None:
        print("没有缓存")
        hot_7_days_blogs = get_seven_hots_read_statistics()
        cache.set('hot_7_days_blogs', hot_7_days_blogs, 3600)
    else:
        print('读取缓存')

    context['seven_read_counts'] = counts
    context['dates'] = dates
    context['todays_hots'] = get_hot_today_read_statistics(contentType)
    context['yesterday_hots'] = get_hot_yestoday_read_statistics(contentType)
    context['seven_read_hots'] = hot_7_days_blogs
    print(context)
    return render(request, 'home.html', context)


def login(request):
    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            user = loginForm.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        loginForm = LoginForm()
    context = {}
    context['loginform'] = loginForm
    return render(request, 'login.html', context)

def register(request):
    pass
