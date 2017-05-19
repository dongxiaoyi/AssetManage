#_*_encoding:utf-8_*_
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from DjangoUeditor.models import UEditorField
from hostlist.models import AccHostList

class MinionLoadAvg(models.Model):
    updatetime = models.CharField(max_length=30, blank=True, verbose_name=u'更新时间')
    minionid = models.CharField(max_length=50, blank=True, verbose_name=u'minionid')
    one = models.CharField(max_length=30, blank=True, verbose_name=u'1 min')
    five = models.CharField(max_length=30, blank=True, verbose_name=u'5 min')
    fifteen = models.CharField(max_length=30, blank=True, verbose_name=u'15 min')
    processes = models.CharField(max_length=30, blank=True, verbose_name=u'运行进程数/总进程数')
    nowprocesspid = models.CharField(max_length=30, blank=True, verbose_name=u'最近运行进程PID')

    class Meta:
        verbose_name = u'minion负载'
        verbose_name_plural = u"minion负载"

    def __unicode__(self):
        return u'%s' %(self.updatetime)

class MasterLoadAvg(models.Model):
    updatetime = models.CharField(max_length=30, blank=True, verbose_name=u'更新时间')
    one = models.CharField(max_length=30, blank=True, verbose_name=u'1 min')
    five = models.CharField(max_length=30, blank=True, verbose_name=u'5 min')
    fifteen = models.CharField(max_length=30, blank=True, verbose_name=u'15 min')
    processes = models.CharField(max_length=30, blank=True, verbose_name=u'运行进程数/总进程数')
    nowprocesspid = models.CharField(max_length=30, blank=True, verbose_name=u'最近运行进程PID')

    class Meta:
        verbose_name = u'master负载'
        verbose_name_plural = u"master负载"

    def __unicode__(self):
        return u'%s' %(self.updatetime)

class MasterProcessStatus(models.Model):
    updatetime = models.CharField(max_length=30, blank=True, verbose_name=u'更新时间')
    status = models.CharField(max_length=30, blank=True, verbose_name=u'状态')

    class Meta:
        verbose_name = u'master进程状态'
        verbose_name_plural = u"master进程状态"

    def __unicode__(self):
        return u'%s' %(self.updatetime)

class MinionOnlineNumber(models.Model):
    updatetime = models.CharField(max_length=30, blank=True, verbose_name=u'更新时间')
    all = models.IntegerField(blank=True, verbose_name=u'总量')
    online = models.IntegerField(blank=True, verbose_name=u'在线')
    offline = models.IntegerField(blank=True, verbose_name=u'离线')

    class Meta:
        verbose_name = u'minion在线数量'
        verbose_name_plural = u'minion在线数量'

    def __unicode__(self):
        return u'%s' %(self.updatetime)