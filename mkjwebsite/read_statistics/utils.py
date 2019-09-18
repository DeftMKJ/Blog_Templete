from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
import datetime
from django.db.models import Sum
from .models import ReadNum, ReadNumDetail


def read_statistics_by_every_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.pk)
    if not request.COOKIES.get(key):
        readout, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readout.read_num += 1
        readout.save()

        date = timezone.now().date()
        print("当前时间%s" % timezone.now())
        read_detail, created = ReadNumDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, read_date=date)
        read_detail.read_num += 1
        read_detail.save()

    return key


def get_seven_days_read_statistics(contentType):
    today = timezone.now().date()
    sevens_counts = []
    dates = []
    for i in range(6, -1, -1):
        deltaDate = today - datetime.timedelta(days=i)
        dates.append(deltaDate.strftime("%m-%d"))
        read_details = ReadNumDetail.objects.filter(content_type=contentType, read_date=deltaDate)
        result =  read_details.aggregate(read_sum=Sum('read_num'))
        sevens_counts.append(result['read_sum'] or 0)
    return dates, sevens_counts
