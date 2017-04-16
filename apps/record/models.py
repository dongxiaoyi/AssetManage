#_*_encoding:utf-8_*_

from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class OperateRecord(models.Model):
    '''
    记录用户操作信息；
    '''
    nowtime = models.DateTimeField(blank=True, null=True, verbose_name=u'操作时间')
    username = models.ForeignKey(User, blank=True, verbose_name=u'用户名')
    user_operate = models.CharField(max_length=100, blank=True, verbose_name=u'操作记录')
    #jid = models.CharField(max_length=255, blank=True, verbose_name=u'jid')

    class Meta:
        verbose_name = u'用户操作信息'
        verbose_name_plural = u"用户操作信息"

    def __unicode__(self):
        return u'%s %s %s' %(self.nowtime, self.username, self.user_operate,)

#class ReturnRecord(models.Model):
#    '''
#    记录用户操作返回结果信息；
#    '''
#
#    jid = models.CharField(max_length=255, blank=True, verbose_name=u'jid')
#    tgt_total = models.CharField(max_length=10, blank=True, verbose_name=u'目标总数')
#    tgt_ret = models.CharField(max_length=10, blank=True, verbose_name=u'有返回结果的主机数量')
#    tgt_succ = models.CharField(max_length=10, blank=True, verbose_name=u'成功的主机数量')
#    tgt_fail = models.CharField(max_length=10, blank=True, verbose_name=u'失败的主机数量')
#    tgt_unret = models.CharField(max_length=10, blank=True, verbose_name=u'未返回结果的主机数量')
#    tgt_unret_list = models.TextField(blank=True, verbose_name=u'未返回结果的主机列表')
#
#    class Meta:
#        verbose_name = u'用户操作返回结果'
#        verbose_name_plural = u"用户操作返回结果"
#
#    def __unicode__(self):
#        return u'%s %s %s %s %s %s' % (self.jid, self.tgt_total, self.tgt_ret, self.tgt_succ, self.tgt_fail, self.tgt_unret)