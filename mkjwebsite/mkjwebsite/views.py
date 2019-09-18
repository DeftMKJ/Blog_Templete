from django.shortcuts import render, get_object_or_404
from read_statistics.utils import get_seven_days_read_statistics
from blogs.models import Blog
from django.contrib.contenttypes.models import ContentType

def home(request):
    context = {}
    dates, counts = get_seven_days_read_statistics(ContentType.objects.get_for_model(Blog))
    context['seven_read_counts'] = counts
    context['dates'] = dates
    print(context)
    return render(request, 'home.html',context)