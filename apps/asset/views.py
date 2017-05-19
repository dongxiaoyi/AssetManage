#_*_encoding:utf-8_*_
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import  ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic.base import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from . import core, models, asset_handle, utils,tables,adminx
from .dashboard import  AssetDashboard
from django.contrib.auth.decorators import login_required
from users.utils.mixin_utils import LoginRequiredMixin
import json
import xadmin
from .models import NewAssetApprovalZone,Asset,CPU,RAM,Disk,Server
# Create your views here.



@csrf_exempt
@utils.token_required
def asset_report(request):
    if request.method == 'POST':
        ass_handler = core.Asset(request)
        if ass_handler.data_is_valid():
            print("----asset data valid:")
            ass_handler.data_inject()
        return HttpResponse(json.dumps(ass_handler.response))
    return HttpResponse('--test--')


@csrf_exempt
def asset_with_no_asset_id(request):
    if request.method == 'POST':
        ass_handler = core.Asset(request)
        res = ass_handler.get_asset_id_by_sn()
        return HttpResponse(json.dumps(res))


def NewAssetApprovalView(request):
    if request.method == 'POST':
        request.POST = request.POST.copy()
        approved_asset_list = request.POST.getlist('approved_asset_list')
        approved_asset_list = NewAssetApprovalZone.objects.filter(id__in=approved_asset_list)
        response_dic = {}
        for obj in approved_asset_list:
            request.POST['asset_data'] = obj.data
            ass_handler = core.Asset(request)
            if Asset.objects.filter(sn=obj.sn) != []:
                new_asset = Asset.objects.create(sn=obj.sn,
                                                 name=obj.sn,
                                                 manufactory=obj.manufactory,
                                                 asset_type=obj.asset_type,
                                                 all_ram_size=obj.ram_size
                                    )
                new_asset.save()
                if obj.cpu_model != None:
                    new_ram = CPU.objects.create(asset=new_asset,cpu_model=obj.model,cpu_count=obj.cpu_count,cpu_core_count=obj.cpu_core_count)
                    new_ram.save()
                if obj.os_type != None:
                    new_os = Server.objects.create(asset=new_asset,os_distribution=obj.os_distribution,os_type=obj.os_type,os_release=obj.os_release)
                    new_os.save()
                NewAssetApprovalZone.objects.filter(sn=obj.sn).delete()
            response_dic[obj.id] = ass_handler.response
        return render(request, 'new_assets_approval.html',
                      {'new_assets': approved_asset_list, 'response_dic': response_dic})
    else:
        ids = request.GET.get('ids')
        id_list = ids.split(',')
        new_assets = models.NewAssetApprovalZone.objects.filter(id__in=id_list)
        return render(request, 'new_assets_approval.html', {'new_assets': new_assets})


class AssetListView(LoginRequiredMixin,View):
    def get(self,request):
        asset_obj_list = tables.table_filter(request, adminx.AssetAdminx, models.Asset)
        # asset_obj_list = models.Asset.objects.all()
        order_res = tables.get_orderby(request, asset_obj_list, adminx.AssetAdminx)
        # print('----->',order_res)
        paginator = Paginator(order_res[0], adminx.AssetAdminx.list_per_page)

        page = request.GET.get('page')
        try:
            asset_objs = paginator.page(page)
        except PageNotAnInteger:
            asset_objs = paginator.page(1)
        except EmptyPage:
            asset_objs = paginator.page(paginator.num_pages)

        table_obj = tables.TableHandler(request,
                                        models.Asset,
                                        adminx.AssetAdminx,
                                        asset_objs,
                                        order_res
                                        )

        return render(request, 'assets.html', {'table_obj': table_obj,
                                               'paginator': paginator})


class GetAssetListView(LoginRequiredMixin,View):
    def gget(self,request):
        asset_dic = asset_handle.fetch_asset_list()
        return HttpResponse(json.dumps(asset_dic, default=utils.json_date_handler))


class AssetCategoryView(LoginRequiredMixin,View):
    def get(self,request):
        category_type = request.GET.get("category_type")
        if not category_type: category_type = 'server'
        if request.is_ajax():
            categories = asset_handle.AssetCategroy(request)
            data = categories.serialize_data()
            return HttpResponse(data)
        else:
            return render(request, 'asset_category.html', {'category_type': category_type})


class AssetEventLogsView(LoginRequiredMixin,View):
    def get(self,request, asset_id):
        log_list = asset_handle.fetch_asset_event_logs(asset_id)
        return HttpResponse(json.dumps(log_list, default=utils.json_datetime_handler))


class AssetDetailView(LoginRequiredMixin,View):
    def get(self,request, asset_id):
        try:
            asset_obj = Asset.objects.get(id=asset_id)
            print asset_obj
        except ObjectDoesNotExist as e:
            return render(request, 'asset_detail.html', {'error': e})
        return render(request, 'asset_detail.html', {"asset_obj": asset_obj})


class GetDashboardDataView(LoginRequiredMixin,View):
    def get(self,request):
        '''返回主页面数据'''
        dashboard_data = AssetDashboard(request)
        dashboard_data.searilize_page()
        return HttpResponse(json.dumps(dashboard_data.data))
