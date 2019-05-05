from django.shortcuts import render
from django.http import HttpResponse
from .tasks import foo

from django_celery_beat.models import PeriodicTask, CrontabSchedule, IntervalSchedule
import json
from django.utils import timezone
import datetime

# Create your views here.
def v_foo(req):
    foo.delay()
    return HttpResponse('Hello!')



def v_new_per_foo_CrontabSchedule(req):
    # PeriodicTask.objects.create(name='v_new_per_foo', task='foo.tasks.per_foo')
    # task任务， created是否定时创建
    task, created = PeriodicTask.objects.get_or_create(name='task_v_new_per_foo', task='foo.tasks.per_foo')

    crontab_time = {
        'month_of_year': 4,  # 月份
        'day_of_month': 10,  # 日期
        'hour': 22,  # 小时
        'minute': 5,  # 分钟
    }
    # 获取 crontab
    crontab = CrontabSchedule.objects.filter(**crontab_time).first()
    if crontab is None:
        # 如果没有就创建，有的话就继续复用之前的crontab
        crontab = CrontabSchedule.objects.create(**crontab_time)
    task.crontab = crontab  # 设置crontab
    task.enabled = True  # 开启task
    task.kwargs = json.dumps({'username': 'zhanhsan'})  # 传入task参数
    expiration = timezone.now() + datetime.timedelta(hours=1)
    task.expires = expiration  # 设置任务过期时间为现在时间的一小时以后
    task.save()
    return HttpResponse('Hello!')


v_new_per_foo = v_new_per_foo_CrontabSchedule

def v_new_per_foo_IntervalSchedule(req):
    # PeriodicTask.objects.create(name='v_new_per_foo', task='foo.tasks.per_foo')
    # task任务， created是否定时创建
    task, created = PeriodicTask.objects.get_or_create(name='task_v_new_per_foo_IntervalSchedule', task='foo.tasks.per_foo')
    interval = IntervalSchedule.objects.create(every=5, period='seconds')
    task.enabled = True  # 开启task
    task.interval = interval
    expiration = timezone.now() + datetime.timedelta(hours=1)
    task.expires = expiration  # 设置任务过期时间为现在时间的一小时以后
    task.save()
    return HttpResponse('Hello!')