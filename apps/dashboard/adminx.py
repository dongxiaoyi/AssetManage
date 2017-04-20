#_*_coding:utf-8_*_
import xadmin
from xadmin import views
from xadmin.views import CommAdminView
from xadmin.plugins.auth import UserAdmin

from .models import MinionLoadAvg,MasterLoadAvg,MasterProcessStatus,MinionOnlineNumber


class MinionLoadAvgAdminx(object):
    list_display = ['updatetime','minionid','one','five','fifteen','processes','nowprocesspid',]
    #搜索框
    search_fields = ['minionid','one','five','fifteen','processes','nowprocesspid']
    #过滤器
    list_filter = ['minionid','one','five','fifteen','processes','nowprocesspid']
    ordering = ['-id']
    #list_editable = ['name']
    #readonly_fields = ['trade_date',]
    refresh_times = [30,50]


class MasterLoadAvgAdminx(object):
    list_display = ['updatetime','one','five','fifteen','processes','nowprocesspid',]
    #搜索框
    search_fields = ['one','five','fifteen','processes','nowprocesspid']
    #过滤器
    list_filter = ['one','five','fifteen','processes','nowprocesspid']
    ordering = ['-id']
    #list_editable = ['name']
    #readonly_fields = ['trade_date',]
    refresh_times = [30,50]

class MasterProcessStatusAdminx(object):
    list_display = ['updatetime','status',]
    #搜索框
    search_fields = ['status',]
    #过滤器
    list_filter = ['status',]
    ordering = ['-id']
    #list_editable = ['name']
    #readonly_fields = ['trade_date',]
    refresh_times = [30,50]

class MinionOnlineNumberAdminx(object):
    list_display = ['updatetime','all','online','offline']
    #搜索框
    search_fields = ['all','online','offline']
    #过滤器
    list_filter = ['all','online','offline']
    ordering = ['-id']
    #list_editable = ['name']
    #readonly_fields = ['trade_date',]
    refresh_times = [30,50]





xadmin.site.register(MinionLoadAvg,MinionLoadAvgAdminx)
xadmin.site.register(MasterLoadAvg,MasterLoadAvgAdminx)
xadmin.site.register(MasterProcessStatus,MasterProcessStatusAdminx)
xadmin.site.register(MinionOnlineNumber,MinionOnlineNumberAdminx)