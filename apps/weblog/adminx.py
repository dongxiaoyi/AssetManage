#_*_coding:utf-8_*_
from django.contrib import admin
import xadmin
from xadmin import views
from xadmin.views import CommAdminView
from xadmin.plugins.auth import UserAdmin
from .models import WebLog,UvModel,PvModel,IvModel


class WebLogAdminx(object):
    list_display = ['logname','remote_addr','remote_user','time_local','method','request','status','body_bytes_sent','http_referer','http_user_agent','add_time']
    #搜索框
    search_fields = ['logname','remote_addr','remote_user','time_local','method','request','status','body_bytes_sent','http_referer','http_user_agent','add_time']
    #过滤器
    list_filter = ['logname','remote_addr','remote_user','time_local','method','request','status','body_bytes_sent','http_referer','http_user_agent']
    #ordering = ['-add_time']
    #list_editable = ['name']
    #readonly_fields = ['trade_date',]
    refresh_times = [3,5]

xadmin.site.register(WebLog,WebLogAdminx)

class UvAdminx(object):
    list_display = ['logname','uv','timestamps']
    #搜索框
    search_fields = ['logname','uv','timestamps']
    #过滤器
    list_filter = ['logname','uv','timestamps']
    ordering = ['-timestamps']
    #list_editable = ['name']
    readonly_fields = ['logname','uv','timestamps']
    refresh_times = [3,5]
    data_charts = {
        "uv": {'title': u"UV", "x-field": "timestamps", "y-field": ("uv"),
                       "order": ('timestamps',)},
    }

xadmin.site.register(UvModel,UvAdminx)

class PvAdminx(object):
    list_display = ['logname','pv','timestamps']
    #搜索框
    search_fields = ['logname','pv','timestamps']
    #过滤器
    list_filter = ['logname','pv','timestamps']
    ordering = ['-timestamps']
    #list_editable = ['name']
    readonly_fields = ['logname','pv','timestamps']
    refresh_times = [3,5]

xadmin.site.register(PvModel,PvAdminx)

class IvAdminx(object):
    list_display = ['logname','iv','timestamps']
    #搜索框
    search_fields = ['logname','iv','timestamps']
    #过滤器
    list_filter = ['logname','iv','timestamps']
    ordering = ['-timestamps']
    #list_editable = ['name']
    readonly_fields = ['logname','iv','timestamps']
    refresh_times = [3,5]

xadmin.site.register(IvModel,IvAdminx)