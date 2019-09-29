from django.shortcuts import render
from django.http import JsonResponse
from .models import LikeCount, LikeRecord
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist


# Create your views here.

def ErrorResponse(code, message):
    res = {}
    res['code'] = '%s' % code
    res['message'] = message
    res['status'] = 'ERROR'
    return JsonResponse(res)


def SuccessResponse(like_num):
    res = {}
    res['status'] = 'SUCCESS'
    res['data'] = like_num
    res['code'] = '%s' % 200
    return JsonResponse(res)


# request拿出来的都是字符串，可以debug看下
def likes_update(request):
    user = request.user
    if not user.is_authenticated:
        ErrorResponse('10001', '用户未登录')

    # 字符串而已
    content_type = request.GET.get('content_type', '')
    object_id = int(request.GET.get('object_id', ''))

    try:
        # 实际对象
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        ErrorResponse('10002', '点赞对象不存在')


    if request.GET.get('is_liked') != 'true':
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        if created:
            total_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            total_count.liked_cound += 1
            total_count.save()
            like_record.save()
            return SuccessResponse(total_count.liked_cound)
        else:
            return ErrorResponse('10003', '不能重复点赞')
    else:
        # 取消点赞
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            like_record.delete()
            total_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created:
                total_count.liked_cound -= 1
                total_count.save()
                return SuccessResponse(total_count.liked_cound)
            else:
                return ErrorResponse(('10004', '点赞数据异常'))
        else:
            return ErrorResponse(('10005', '未点赞过，不能取消点赞'))
