#_*_coding:utf-8_*_
from django.contrib import admin
import xadmin
from xadmin import views
from xadmin.views import CommAdminView
from xadmin.plugins.auth import UserAdmin
from .models import Asset,Server,SecurityDevice,NetworkDevice,Software,CPU,RAM,Disk,NIC,RaidAdaptor,BusinessUnit,IDC,Contract,Tag,NewAssetApprovalZone
#from .models import EventLog

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSetrtings(object):
    site_title = "AssetManage管理后台"
    site_footer = 'AssetManage'
    menu_style = "accordion"


xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSetrtings)





class ServerInline(object):
    model = Server
    extra = 0
    exclude = ('memo',)
    readonly_fields = ['create_date']


class CPUInline(object):
    model = CPU
    extra = 0
    exclude = ('memo',)
    readonly_fields = ['create_date']


class NICInline(object):
    model = NIC
    extra = 0
    exclude = ('memo',)
    readonly_fields = ['create_date']


class RAMInline(object):
    model = RAM
    extra = 0
    exclude = ('memo',)
    readonly_fields = ['create_date']


class DiskInline(object):
    model = Disk
    extra = 0
    exclude = ('memo',)
    readonly_fields = ['create_date']


class AssetAdminx(object):
    list_display = ['id','asset_type','sn','name','all_ram_size','manufactory','manufactory_support_num','management_ip','idc','business_unit','admin','trade_date','status']
    #搜索框
    search_fields = ['sn']
    #过滤器
    list_filter = ['asset_type','sn','name','manufactory','management_ip','idc','business_unit','admin','trade_date','status']
    choice_fields = ['asset_type', 'status']
    fk_fields = ['manufactory', 'idc', 'business_unit', 'admin']
    list_per_page = 10
    readonly_fields = ['trade_date',]
    inlines = [ServerInline,CPUInline,NICInline,RAMInline,DiskInline]
    style_fields = {'memo':'ueditor'}
    dynamic_fk = 'asset_type'
    dynamic_list_display = ('model','sub_asset_type','os_type','os_distribution')
    dynamic_choice_fields = ('sub_asset_type',)
    m2m_fields = ('tags',)


class ServerAdminx(object):
    list_display = ['id','asset','sub_asset_type','created_by','hosted_on','model','raid_type','os_type','os_distribution','os_release','create_date','update_date']
    #搜索框
    search_fields = ['id','asset','sub_asset_type','created_by','hosted_on','model','raid_type','os_type','os_distribution','os_release']
    #过滤器
    list_filter = ['asset','sub_asset_type','created_by','hosted_on','model','raid_type','os_type','os_distribution','os_release']
    ordering = ['-id']
    #list_editable = ['name']
    #readonly_fields = ['trade_date',]
    refresh_times = [3,5]
    #style_fields = {'memo':'ueditor'}


class SecurityDeviceAdminx(object):
    list_display = ['id','asset','sub_asset_type']
    #搜索框
    search_fields = ['id','asset','sub_asset_type']
    #过滤器
    list_filter = ['asset','sub_asset_type']
    ordering = ['-id']
    #list_editable = ['name']
    #readonly_fields = ['trade_date',]
    refresh_times = [3,5]
    #style_fields = {'memo':'ueditor'}


class NetworkDeviceadminx(object):
    list_display = ['id','asset','sub_asset_type','vlan_ip','intranet_ip','model','firmware','port_num','device_detail']
    #搜索框
    search_fields = ['id','asset','sub_asset_type','vlan_ip','intranet_ip','model','firmware','port_num','device_detail']
    #过滤器
    list_filter = ['asset','sub_asset_type','vlan_ip','intranet_ip','model','firmware','port_num','device_detail']
    ordering = ['-id']
    #list_editable = ['name']
    #readonly_fields = ['trade_date',]
    refresh_times = [3,5]
    style_fields = {'device_detail':'ueditor'}


class SoftwareAdminx(object):
    list_display = ['id','sub_asset_type','version']
    #搜索框
    search_fields = ['id','sub_asset_type','version']
    #过滤器
    list_filter = ['sub_asset_type','version']
    ordering = ['-id']
    #list_editable = ['name']
    #readonly_fields = ['trade_date',]
    refresh_times = [3,5]
    #style_fields = {'device_detail':'ueditor'}


class CPUAdminx(object):
    list_display = ['id','asset','cpu_model','cpu_count','cpu_core_count','memo','create_date','update_date']
    #搜索框
    search_fields = ['id','asset','cpu_model','cpu_count','cpu_core_count','memo']
    #过滤器
    list_filter = ['asset','cpu_model','cpu_count','cpu_core_count']
    ordering = ['-id']
    #list_editable = ['name']
    #readonly_fields = ['trade_date',]
    refresh_times = [3,5]
    style_fields = {'memo':'ueditor'}


class RAMAdminx(object):
    list_display = ['id','asset','sn','model','slot','capacity','memo','create_date','update_date']
    #搜索框
    search_fields = ['sn','model','slot','capacity']
    #过滤器
    list_filter = ['sn','model','slot','capacity']
    ordering = ['-id']
    list_editable = ['name']
    #readonly_fields = ['trade_date',]
    refresh_times = [3,5]
    #style_fields = {'memo':'ueditor'}


class DiskAdminx(object):
    list_display = ['id','asset','sn','model','slot','manufactory','capacity','iface_type','memo','create_date','update_date']
    #搜索框
    search_fields = ['id','asset','sn','model','slot','manufactory','capacity','iface_type','memo']
    #过滤器
    list_filter = ['asset','sn','model','slot','manufactory','capacity','iface_type']
    ordering = ['-id']
    #list_editable = ['name']
    #readonly_fields = ['trade_date',]
    refresh_times = [3,5]
    style_fields = {'memo':'ueditor'}


class NICAdminx(object):
    list_display = ['id','asset','name','sn','model','macaddress','ipaddress','netmask','bonding','memo','create_date','update_date']
    #搜索框
    search_fields = ['id','asset','sn','model','macaddress','ipaddress','netmask','bonding','memo']
    #过滤器
    list_filter = ['asset','sn','model','macaddress','ipaddress','netmask','bonding']
    ordering = ['-id']
    list_editable = ['name']
    #readonly_fields = ['trade_date',]
    refresh_times = [3,5]
    style_fields = {'memo':'ueditor'}


class RaidAdaptorAdminx(object):
    list_display = ['id','asset','sn','slot','model','memo','create_date','update_date']
    #搜索框
    search_fields = ['id','asset','sn','slot','model','memo']
    #过滤器
    list_filter = ['asset','sn','slot','model']
    ordering = ['-id']
    #list_editable = ['name']
    #readonly_fields = ['trade_date',]
    refresh_times = [3,5]
    style_fields = {'memo':'ueditor'}


class ManufactoryAdminx(object):
    list_display = ['id','manufactory','support_num','memo']
    #搜索框
    search_fields = ['id','manufactory','support_num','memo']
    #过滤器
    list_filter = ['manufactory','support_num']
    ordering = ['-id']
    list_editable = ['manufactory','support_num']
    #readonly_fields = ['trade_date',]
    refresh_times = [3,5]
    style_fields = {'memo':'ueditor'}


class BusinessUnitAdminx(object):
    list_display = ['id','parent_unit','name','memo']
    #搜索框
    search_fields = ['id','name','memo']
    #过滤器
    list_filter = ['name','memo']
    ordering = ['-id']
    list_editable = ['name']
    #readonly_fields = ['trade_date',]
    refresh_times = [3,5]
    style_fields = {'memo':'ueditor'}


class ContractAdminx(object):
    list_display = ['id','sn','name','price','detail','start_date','end_date','license_num','memo','create_date','update_date']
    #搜索框
    search_fields = ['id','sn','name','price','detail']
    #过滤器
    list_filter = ['sn','name','price','detail']
    ordering = ['-id']
    list_editable = ['name']
    #readonly_fields = ['trade_date',]
    refresh_times = [3,5]
    style_fields = {'memo':'ueditor','detail':'ueditor'}


class IDCAdminx(object):
    list_display = ['id','name','memo']
    #搜索框
    search_fields = ['id','name','memo']
    #过滤器
    list_filter = ['name']
    ordering = ['-id']
    list_editable = ['name']
    #readonly_fields = ['trade_date',]
    refresh_times = [3,5]
    style_fields = {'memo':'ueditor'}


class TagAdminx(object):
    list_display = ['id','name','creater','create_date']
    #搜索框
    search_fields = ['id','name','creater']
    #过滤器
    list_filter = ['name','creater']
    ordering = ['-id']
    list_editable = ['name']
    #readonly_fields = ['trade_date',]
    refresh_times = [3,5]
    #style_fields = {'memo':'ueditor'}


#class EventLogAdminx(object):
#    list_display = ['name','colored_event_type','asset','component','detail','date','user']
#    search_fields = ['asset',]
#    list_filter = ['event_type','component','date','user']

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
class NewAssetApprovalZoneAdminx(object):
    list_display = ['sn', 'asset_type', 'manufactory', 'model', 'cpu_model', 'cpu_count', 'cpu_core_count', 'ram_size',
                    'os_distribution', 'os_release', 'date', 'approved', 'approved_by', 'approved_date']
    actions = ['approve_selected_objects']

    def approve_selected_objects(modeladmin, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        ct = ContentType.objects.get_for_model(queryset.model)
        return HttpResponseRedirect("/asset/new_assets_approval/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))

    approve_selected_objects.short_description = "批准入库"


xadmin.site.register(Asset,AssetAdminx)
xadmin.site.register(Server,ServerAdminx)
xadmin.site.register(SecurityDevice,SecurityDeviceAdminx)
xadmin.site.register(Software,SoftwareAdminx)
xadmin.site.register(CPU,CPUAdminx)
xadmin.site.register(RAM,RAMAdminx)
xadmin.site.register(Disk,DiskAdminx)
xadmin.site.register(NIC,NICAdminx)
xadmin.site.register(NetworkDevice,NetworkDeviceadminx)
xadmin.site.register(RaidAdaptor,RaidAdaptorAdminx)
xadmin.site.register(BusinessUnit,BusinessUnitAdminx)
xadmin.site.register(IDC,IDCAdminx)
xadmin.site.register(Contract,ContractAdminx)
xadmin.site.register(Tag,TagAdminx)
#xadmin.site.register(EventLog,EventLogAdminx)
xadmin.site.register(NewAssetApprovalZone,NewAssetApprovalZoneAdminx)