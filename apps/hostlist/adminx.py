#_*_coding:utf-8_*_
import xadmin
from xadmin import views
from xadmin.views import CommAdminView
from xadmin.plugins.auth import UserAdmin

from .models import AccHostList,UnAccHostList, Dzhuser, DataCenter, NetworkOperator, ProvinceArea, Catagory,ErrorHostList

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

class CatagoryAdminx(object):
    list_display = ['catagoryen','catagorycn']
    #搜索框
    search_fields = ['catagoryen','catagorycn']
    #过滤器
    list_filter = ['catagoryen','catagorycn']
    ordering = ['-catagoryen']
    #list_editable = ['name']
    #readonly_fields = ['trade_date',]
    refresh_times = [3,5]

class UnAccHostListAdminx(object):
    list_display = ['ip','hostname','minionid','nocn','dccn','engineer','mac_id','zsourceip','bsourceip','licdate','licstatus','idip','ipsame','remark','action']
    #搜索框
    search_fields = ['ip','hostname','minionid','nocn','dccn','engineer','mac_id','zsourceip','bsourceip','licdate','licstatus','idip','ipsame','remark']
    #过滤器
    list_filter = ['ip','hostname','minionid','nocn','dccn','engineer','mac_id','zsourceip','bsourceip','licdate','licstatus','idip','ipsame','remark']
    ordering = ['-hostname']
    list_per_page = 10
    choice_fields = []
    fk_fields = ['ip','hostname','minionid']
    #list_editable = ['name']
    #readonly_fields = ['action',]
    refresh_times = [3,5]

    def queryset(self):
        qs = super(UnAccHostListAdminx,self).queryset()
        qs = qs.filter(key_tag='unacc')
        return qs


class AccHostListAdminx(object):
    list_display = ['ip','hostname','minionid','nocn','dccn','engineer','mac_id','zsourceip','bsourceip','licdate','licstatus','idip','ipsame','remark','action']
    #搜索框
    search_fields = ['ip','hostname','minionid','nocn','dccn','engineer','mac_id','zsourceip','bsourceip','licdate','licstatus','idip','ipsame','remark']
    #过滤器
    list_filter = ['ip','hostname','minionid','nocn','dccn','engineer','mac_id','zsourceip','bsourceip','licdate','licstatus','idip','ipsame','remark']
    ordering = ['-hostname']
    list_per_page = 10
    choice_fields = []
    fk_fields = ['ip','hostname','minionid']
    #list_editable = ['name']
    #readonly_fields = ['action',]
    refresh_times = [3,5]

    def queryset(self):
        qs = super(AccHostListAdminx,self).queryset()
        qs = qs.filter(key_tag='acc')
        return qs

class ErrorHostListAdminx(object):
    list_display = ['ip','hostname','minionid','nocn','dccn','engineer','mac_id','zsourceip','bsourceip','licdate','licstatus','idip','ipsame','remark','action']
    #搜索框
    search_fields = ['ip','hostname','minionid','nocn','dccn','engineer','mac_id','zsourceip','bsourceip','licdate','licstatus','idip','ipsame','remark']
    #过滤器
    list_filter = ['ip','hostname','minionid','nocn','dccn','engineer','mac_id','zsourceip','bsourceip','licdate','licstatus','idip','ipsame','remark']
    ordering = ['-hostname']
    list_per_page = 10
    choice_fields = []
    fk_fields = ['ip','hostname','minionid']
    #list_editable = ['name']
    #readonly_fields = ['action',]
    refresh_times = [3,5]

    def queryset(self):
        qs = super(ErrorHostListAdminx,self).queryset()
        qs = qs.filter(key_tag='error')
        return qs

xadmin.site.register(AccHostList,AccHostListAdminx)
xadmin.site.register(UnAccHostList,UnAccHostListAdminx)
xadmin.site.register(ErrorHostList,ErrorHostListAdminx)

xadmin.site.register(Dzhuser,DzhuserAdminx)
xadmin.site.register(DataCenter,DataCenterAdminx)
xadmin.site.register(NetworkOperator,NetworkOperatorAdminx)
xadmin.site.register(ProvinceArea,ProvinceAreaAdminx)
xadmin.site.register(Catagory,CatagoryAdminx)