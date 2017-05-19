#_*_coding:utf-8_*_
import xadmin
from xadmin import views
from xadmin.views import CommAdminView
from xadmin.plugins.auth import UserAdmin

from .models import MinionGroups,AccHostList,UnAccHostList, Dzhuser, DataCenter, NetworkOperator, ProvinceArea, ErrorHostList


class DzhuserAdminx(object):
    list_display = ['username','engineer']
    #搜索框
    search_fields = ['username','engineer']
    #过滤器
    list_filter = ['username','engineer']
    ordering = ['-username']
    #list_editable = ['name']
    #readonly_fields = ['trade_date',]
    refresh_times = [3,5]

class DataCenterAdminx(object):
    list_display = ['dcen','dccn']
    #搜索框
    search_fields = ['dcen','dccn']
    #过滤器
    list_filter = ['dcen','dccn']
    ordering = ['-dcen']
    #list_editable = ['name']
    #readonly_fields = ['trade_date',]
    refresh_times = [3,5]

class NetworkOperatorAdminx(object):
    list_display = ['noen','nocn']
    #搜索框
    search_fields = ['noen','nocn']
    #过滤器
    list_filter = ['noen','nocn']
    ordering = ['-noen']
    #list_editable = ['name']
    #readonly_fields = ['trade_date',]
    refresh_times = [3,5]

class ProvinceAreaAdminx(object):
    list_display = ['paen','pacn']
    #搜索框
    search_fields = ['paen','pacn']
    #过滤器
    list_filter = ['paen','pacn']
    ordering = ['-paen']
    #list_editable = ['name']
    #readonly_fields = ['trade_date',]
    refresh_times = [3,5]

class UnAccHostListAdminx(object):
    list_display = ['id','minionid','remark','action']
    #搜索框
    search_fields = ['id','minionid','remark','action']
    #过滤器
    list_filter = ['id','minionid','remark','action']
    ordering = ['-minionid']
    list_per_page = 10
    choice_fields = []
    fk_fields = ['minionid',]
    #list_editable = ['name']
    #readonly_fields = ['action',]
    refresh_times = [3,5]

class MinionGroupsAdminx(object):
    list_display = ['Group','minion']
    refresh_times = [3, 5]
    list_editable = ['Group']


class AccHostListAdminx(object):
    list_display = ['minionid','wip','nip','hostname','osfinger','mem_total','cpu_model','cpuarch','num_cpus','kernelrelease','nocn', 'engineer','saltversion','remark','action']
    #搜索框
    search_fields = ['minionid','wip','nip','hostname','osfinger','mem_total','cpu_model','cpuarch','kernelrelease','nocn', 'engineer','saltversion','remark']
    #过滤器
    list_filter = ['minionid','wip','nip','hostname','osfinger','mem_total','cpu_model','cpuarch','kernelrelease','nocn', 'engineer','saltversion','remark']
    ordering = ['-minionid']
    list_per_page = 10
    choice_fields = []
    fk_fields = ['wip','hostname','minionid']
    #list_editable = ['name']
    #readonly_fields = ['action',]
    refresh_times = [3,5]



class ErrorHostListAdminx(object):
    list_display = ['id','minionid','remark','action']
    #搜索框
    search_fields = ['id','minionid','remark','action']
    #过滤器
    list_filter = ['id','minionid','remark','action']
    ordering = ['-minionid']
    list_per_page = 10
    choice_fields = []
    fk_fields = ['minionid',]
    #list_editable = ['name']
    #readonly_fields = ['action',]
    refresh_times = [3,5]


xadmin.site.register(AccHostList,AccHostListAdminx)
xadmin.site.register(UnAccHostList,UnAccHostListAdminx)
xadmin.site.register(ErrorHostList,ErrorHostListAdminx)
xadmin.site.register(MinionGroups,MinionGroupsAdminx)

xadmin.site.register(Dzhuser,DzhuserAdminx)
xadmin.site.register(DataCenter,DataCenterAdminx)
xadmin.site.register(NetworkOperator,NetworkOperatorAdminx)
xadmin.site.register(ProvinceArea,ProvinceAreaAdminx)


