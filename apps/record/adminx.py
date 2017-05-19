#_*_coding:utf-8_*_
import xadmin
from xadmin import views
from xadmin.views import CommAdminView
from xadmin.plugins.auth import UserAdmin

from .models import OperateRecord

class OperateRecordAdminx(object):
    list_display = ['nowtime','username','user_operate']
    #搜索框
    search_fields = ['username','user_operate']
    #过滤器
    list_filter = ['nowtime','username','user_operate']
    ordering = ['-nowtime']
    #list_editable = ['name']
    #readonly_fields = ['trade_date',]
    refresh_times = [3,5]

##class ReturnRecordAdminx(object):
#    list_display = ['jid','tgt_total','tgt_ret','tgt_succ','tgt_fail','tgt_unret','tgt_unret_list']
#    #搜索框
#    search_fields = ['jid','tgt_total','tgt_ret','tgt_succ','tgt_fail','tgt_unret','tgt_unret_list']
#    #过滤器
#    list_filter = ['jid','tgt_total','tgt_ret','tgt_succ','tgt_fail','tgt_unret','tgt_unret_list']
#    ordering = ['-jid']
#    #list_editable = ['name']
#    #readonly_fields = ['trade_date',]
#    refresh_times = [3,5]

#xadmin.site.register(ReturnRecord,ReturnRecordAdminx)
xadmin.site.register(OperateRecord,OperateRecordAdminx)