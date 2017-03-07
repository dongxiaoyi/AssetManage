# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Dzhuser(models.Model):
    username = models.ForeignKey(User, blank=True, verbose_name=u'用户名')
    engineer = models.CharField(max_length=30, blank=True, verbose_name=u'维护人员')

    class Meta:
        verbose_name = u'维护人员列表'
        verbose_name_plural = u"维护人员列表"

    def __unicode__(self):
        return u'%s %s' %(self.username, self.engineer)

class DataCenter(models.Model):
    dcen = models.CharField(max_length=30, blank=True, verbose_name=u'机房简称')
    dccn = models.CharField(max_length=30, blank=True, verbose_name=u'机房全称')

    class Meta:
        verbose_name = u'机房列表'
        verbose_name_plural = u"机房列表"

    def __unicode__(self):
        return u'%s %s' %(self.dcen, self.dccn)

class NetworkOperator(models.Model):
    noen = models.CharField(max_length=30, blank=True, verbose_name=u'运营商简称')
    nocn = models.CharField(max_length=30, blank=True, verbose_name=u'运营商全称')

    class Meta:
        verbose_name = u'运营商列表'
        verbose_name_plural = u"运营商列表"

    def __unicode__(self):
        return u'%s %s' %(self.noen, self.nocn)

class ProvinceArea(models.Model):
    paen = models.CharField(max_length=30, blank=True, verbose_name=u'省份地区简称')
    pacn = models.CharField(max_length=30, blank=True, verbose_name=u'省份地区全称')

    class Meta:
        verbose_name = u'城市列表'
        verbose_name_plural = u"城市列表"

    def __unicode__(self):
        return u'%s %s' %(self.paen, self.pacn)

class Catagory(models.Model):
    catagoryen = models.CharField(max_length=30, blank=True, verbose_name=u'类别简称')
    catagorycn = models.CharField(max_length=30, blank=True, verbose_name=u'类别全称')

    class Meta:
        verbose_name = u'分类列表'
        verbose_name_plural = u"分类列表"

    def __unicode__(self):
        return u'%s %s' %(self.catagoryen, self.catagorycn)

class UnAccHostList(models.Model):
    ip = models.CharField(max_length=15,  blank=True,null=True,verbose_name=u'IP地址')
    hostname = models.CharField(max_length=30, verbose_name=u'主机名')
    minionid = models.CharField(max_length=60, verbose_name=u'MinionID')
    is_acc = models.BooleanField(default=False,verbose_name=u'是否结束minion_id')
    nocn = models.ForeignKey(NetworkOperator,blank=True,null=True, verbose_name=u'运营商全称')
    catagorycn = models.ForeignKey(Catagory, blank=True,null=True, verbose_name=u'类别')
    pacn = models.ForeignKey(ProvinceArea, blank=True,null=True,verbose_name=u'地区全称')
    dccn = models.ForeignKey(DataCenter, blank=True,null=True, verbose_name=u'机房全称')
    engineer = models.ForeignKey(Dzhuser, blank=True,null=True, verbose_name=u'维护人员')
    mac_id = models.CharField(max_length=20,  blank=True,null=True,verbose_name=u'MAC地址')
    zsourceip = models.CharField(max_length=30,  blank=True,null=True,verbose_name=u'主行情源')
    bsourceip = models.CharField(max_length=30,  blank=True,null=True,verbose_name=u'备行情源')
    #dccn = models.ForeignKey(dataCenter, related_name='datacenter_hostlist')
    licdate = models.CharField(max_length=30,  blank=True,null=True,verbose_name=u'授权日期')
    licstatus = models.CharField(max_length=30, blank=True,null=True, verbose_name=u'授权状态')
    #engineer = models.ForeignKey(dzhuser, related_name='dzhuser_hostlist')
    idip = models.CharField(max_length=15,  blank=True,null=True,verbose_name=u'MinionID中的IP地址')
    ipsame = models.CharField(max_length=10,  blank=True,null=True,verbose_name=u'IP地址一致性')
    remark = models.TextField(max_length=200, blank=True,null=True, verbose_name=u'备注')

    def __unicode__(self):
        return u'%s %s %s %s %s' %(self.hostname, self.ip, self.catagorycn, self.dccn, self.engineer)
    class Meta:
        ordering = ['minionid']
        verbose_name = u'已验证minion_id列表'
        verbose_name_plural = u"Host列表-验证salt_id"

class AccHostList(UnAccHostList):
    class Meta:
        verbose_name = '未验证minion_id列表'
        verbose_name_plural = verbose_name
        proxy = True