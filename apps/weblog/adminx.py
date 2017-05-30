#_*_coding:utf-8_*_
from django.contrib import admin
import xadmin
from xadmin import views
from xadmin.views import CommAdminView
from xadmin.plugins.auth import UserAdmin
from .models import WebLog


class WebLogAdminx(object):
    list_display = ['logname','remote_addr','remote_user','time_local','method','request','status','body_bytes_sent','http_referer','http_user_agent','add_time']
    #搜索框
    search_fields = ['logname','remote_addr','remote_user','time_local','method','request','status','body_bytes_sent','http_referer','http_user_agent','add_time']
    #过滤器
    list_filter = ['logname','remote_addr','remote_user','time_local','method','request','status','body_bytes_sent','http_referer','http_user_agent']

xadmin.site.register(WebLog,WebLogAdminx)

