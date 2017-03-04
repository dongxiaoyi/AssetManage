#_*_coding:utf-8_*_
from django.contrib import admin
import xadmin
from xadmin import views
from xadmin.views import CommAdminView
from xadmin.plugins.auth import UserAdmin
from .models import EmaliVerifyRecord,UserMessage


class EmaliVerifyRecordAdmin(object):
    list_display = ['code','email','send_type','send_time',]
    #搜索框
    search_fields = ['code','email','send_type']
    #过滤器
    list_filter = ['code','email','send_type','send_time',]
    model_icon = 'fa fa-address-card-o'

xadmin.site.register(EmaliVerifyRecord,EmaliVerifyRecordAdmin)

class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    list_filter = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read']

xadmin.site.register(UserMessage, UserMessageAdmin)
