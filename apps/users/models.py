#_*_encoding:utf-8_*_
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from DjangoUeditor.models import UEditorField


class ProfileBase(type):
    def __new__(cls, name, bases, attrs):
        module = attrs.pop('__module__')
        parents = [b for b in bases if isinstance(b, ProfileBase)]
        if parents:
            fields = []
            for obj_name, obj in attrs.items():
                if isinstance(obj, models.Field): fields.append(obj_name)
                User.add_to_class(obj_name, obj)
            UserAdmin.fieldsets = list(UserAdmin.fieldsets)
            UserAdmin.fieldsets.append((name, {'fields': fields}))
        return super(ProfileBase, cls).__new__(cls, name, bases, attrs)

class Profile(object):
    __metaclass__ = ProfileBase
# Create your models here.

class MyUser(Profile):
    image = models.ImageField(upload_to="image/%Y/%m",default=u'image/defaule.png',max_length=100,verbose_name=u'头像')
    token = models.CharField(u'token', max_length=128, default=None, blank=True, null=True)
    department = models.CharField(u'部门', max_length=32, default=None, blank=True, null=True)
    # business_unit = models.ManyToManyField(BusinessUnit)
    tel = models.CharField(u'座机', max_length=32, default=None, blank=True, null=True)
    mobile = models.CharField(u'手机', max_length=32, default=None, blank=True, null=True)
    gender = models.CharField(choices=(('male',u'男'),('female',u'女')),default='female',max_length=6,verbose_name=u'性别')
    is_active = True
    memo = models.TextField(u'备注', blank=True, null=True, default=None)

    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name

    def unread_nums(self):
        # 获取用户未读消息的数量
        return UserMessage.objects.filter(user=self.id, has_read=False ).count()

    def is_today_birthday(self):
        return self.birthday.date() == datetime.date.today()

    def __unicode__(self):
        return self.username

class EmaliVerifyRecord(models.Model):
    code = models.CharField(max_length=20,verbose_name=u'验证码')
    email = models.EmailField(max_length=50,verbose_name=u'邮箱')
    send_type = models.CharField(verbose_name=u'验证码类型',choices=(('register',u'注册'),('forget',u'找回密码'),('up_email',u'修改邮箱')),max_length=10)
    send_time = models.DateTimeField(verbose_name='发送时间',default=datetime.now)

    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}({1})'.format(self.code,self.email)

class UserMessage(models.Model):
    user = models.ForeignKey(User, verbose_name=u"接受用户")
    message = models.CharField(max_length=500, verbose_name=u"消息内容")
    has_read = models.BooleanField(default=False, verbose_name=u"是否已读")
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户消息"
        verbose_name_plural = verbose_name