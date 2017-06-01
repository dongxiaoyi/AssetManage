#_*_encoding:utf-8_*_
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class WebLog(models.Model):
    logname =  models.CharField(max_length=255,verbose_name=u'log名称')
    remote_addr = models.CharField(max_length=15,verbose_name=u'目标IP')
    remote_user = models.CharField(max_length=255,verbose_name=u'目标用户')
    time_local = models.CharField(max_length=255,verbose_name=u'本地时间')
    method = models.CharField(max_length=255,verbose_name=u'方法')
    request = models.CharField(max_length=255,verbose_name=u'request')
    status = models.CharField(max_length=255,verbose_name=u'状态')
    body_bytes_sent = models.CharField(max_length=255,verbose_name=u'主体大小')
    http_referer = models.CharField(max_length=255,verbose_name=u'来自链接')
    http_user_agent = models.CharField(max_length=255,verbose_name=u'客户端')
    #下面日期格式化到年月日来存储pv，uv，ip
    timestamps = models.CharField(max_length=255,verbose_name=u'统计时间戳')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")

    class Meta:
        verbose_name = u'WebLog'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.logname

class UvModel(models.Model):
    logname =  models.CharField(max_length=255,verbose_name=u'log名称')
    uv = models.IntegerField(verbose_name=u'UV')
    timestamps = models.CharField(max_length=255, verbose_name=u'统计时间戳')

    def __unicode__(self):
        return self.logname

class PvModel(models.Model):
    logname =  models.CharField(max_length=255,verbose_name=u'log名称')
    pv = models.IntegerField(verbose_name=u'PV')
    timestamps = models.CharField(max_length=255, verbose_name=u'统计时间戳')

    def __unicode__(self):
        return self.logname

class IvModel(models.Model):
    logname =  models.CharField(max_length=255,verbose_name=u'log名称')
    iv = models.IntegerField(verbose_name=u'IV')
    timestamps = models.CharField(max_length=255, verbose_name=u'统计时间戳')

    def __unicode__(self):
        return self.logname