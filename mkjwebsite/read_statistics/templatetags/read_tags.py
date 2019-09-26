from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import ReadNum
from django.db.models.fields import exceptions

register = template.Library()


@register.simple_tag
def get_total_read_count(obj):
    try:
        ct = ContentType.objects.get_for_model(obj)
        readnum = ReadNum.objects.get(content_type=ct, object_id=obj.pk)
        return readnum.read_num
    except exceptions.ObjectDoesNotExist:
        return 0