# _*_encoding:utf-8_*_
from __future__ import unicode_literals

from django.db import models
# Create your models here.
from DjangoUeditor.models import UEditorField
#from saltstack.models import Service

class UploadFiles(models.Model):
    name = models.CharField(verbose_name=u'文件名',max_length=50,blank=True,null=True)
    #groups = models.ManyToManyField(Service,blank=True,null=True,verbose_name='所属服务')


    class Meta:
        verbose_name = u'上传文件'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name