#_*_coding:utf-8_*_
import xadmin
from xadmin import views
from xadmin.views import CommAdminView
from xadmin.plugins.auth import UserAdmin
from .models import Service

class ServiceAdminx(object):
    list_display = ['name','envtag','minions','groups','sls','file']
    #搜索框
    search_fields = ['name','envtag','minions','groups']
    #过滤器
    list_filter = ['name','envtag','minions','groups']
    ordering = ['-name']
    list_editable = ['name','envtag']
    #readonly_fields = ['trade_date',]
    refresh_times = [3,5]
    #style_fields = {'sls': 'ueditor',}

xadmin.site.register(Service,ServiceAdminx)

#from .models import DangerCommand, ModulesLock, DeployModules, ConfigUpdate, CommonOperate
#
#class DangerCommandAdminx(object):
#    list_display = ['command','status']
#    #搜索框
#    search_fields = ['command','status']
#    #过滤器
#    list_filter = ['command','status']
#    ordering = ['-command']
#    #list_editable = ['name']
#    #readonly_fields = ['trade_date',]
#    refresh_times = [3,5]
#
#class ModulesLockAdminx(object):
#    list_display = ['module','status','user']
#    #搜索框
#    search_fields = ['module','status','user']
#    #过滤器
#    list_filter = ['module','status','user']
#    ordering = ['-module']
#    #list_editable = ['name']
#    #readonly_fields = ['trade_date',]
#    refresh_times = [3,5]
#
#class DeployModulesAdminx(object):
#    list_display = ['module','slsfile']
#    #搜索框
#    search_fields = ['module','slsfile']
#    #过滤器
#    list_filter = ['module','slsfile']
#    ordering = ['-module']
#    #list_editable = ['name']
#    #readonly_fields = ['trade_date',]
#    refresh_times = [3,5]
#
#class ConfigUpdateAdminx(object):
#    list_display = ['module','slsfile']
#    #搜索框
#    search_fields = ['module','slsfile']
#    #过滤器
#    list_filter = ['module','slsfile']
#    ordering = ['-module']
#    #list_editable = ['name']
#    #readonly_fields = ['trade_date',]
#    refresh_times = [3,5]
#
#class CommonOperateAdminx(object):
#    list_display = ['module','slsfile']
#    #搜索框
#    search_fields = ['module','slsfile']
#    #过滤器
#    list_filter = ['module','slsfile']
#    ordering = ['-module']
#    #list_editable = ['name']
#    #readonly_fields = ['trade_date',]
#    refresh_times = [3,5]
#
#xadmin.site.register(DangerCommand,DangerCommandAdminx)
#xadmin.site.register(ModulesLock,ModulesLockAdminx)
#xadmin.site.register(DeployModules,DeployModulesAdminx)
#xadmin.site.register(ConfigUpdate,ConfigUpdateAdminx)
#xadmin.site.register(CommonOperate,CommonOperateAdminx)
#