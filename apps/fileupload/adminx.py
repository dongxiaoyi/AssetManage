#_*_coding:utf-8_*_
import xadmin
from xadmin import views
from xadmin.views import CommAdminView
from xadmin.plugins.auth import UserAdmin
from .models import UploadFiles

class UploadFilesAdminx(object):
    list_display = ['name']
    #搜索框
    search_fields = ['name']
    #过滤器
    list_filter = ['name']
    ordering = ['-name']
    list_editable = ['name']
    #readonly_fields = ['trade_date',]
    refresh_times = [3,5]
    #style_fields = {'sls': 'ueditor',}

xadmin.site.register(UploadFiles,UploadFilesAdminx)