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
from . import models,adminx
from django.contrib.auth.decorators import login_required
from users.utils.mixin_utils import LoginRequiredMixin
import json,logging
import xadmin
from .models import Dzhuser, DataCenter, AccHostList,UnAccHostList,ErrorHostList
from asset import tables
from .adminx import AccHostListAdminx,UnAccHostListAdminx,ErrorHostListAdminx
from hostlist.models import MinionGroups
from .forms import CreateGroupsForm,MinionToGroupForm

class AccMinionListView(LoginRequiredMixin,View):
    def get(self,request):
        #acc_obj_list = tables.table_filter(request, adminx.AccHostListAdminx, models.AccHostList)
        acc_obj_list = AccHostList.objects.filter(key_tag='acc')

        # asset_obj_list = models.Asset.objects.all()
        order_res = tables.get_orderby(request, acc_obj_list, adminx.AccHostListAdminx)
        # print('----->',order_res)
        paginator = Paginator(order_res[0], adminx.AccHostListAdminx.list_per_page)

        page = request.GET.get('page')
        try:
            acc_objs = paginator.page(page)
        except PageNotAnInteger:
            acc_objs = paginator.page(1)
        except EmptyPage:
            acc_objs = paginator.page(paginator.num_pages)

        table_obj = tables.TableHandler(request,
                                        models.AccHostList,
                                        adminx.AccHostListAdminx,
                                        acc_objs,
                                        order_res
                                        )
        return render(request, 'salt_acc_minion.html', {'table_obj': table_obj,
                                               'paginator': paginator})


class UnAccMinionListView(LoginRequiredMixin,View):
    def get(self,request):
        unacc_obj_list = UnAccHostList.objects.filter(key_tag='unacc')
        # asset_obj_list = models.Asset.objects.all()
        order_res_list = tables.get_orderby(request, unacc_obj_list, adminx.UnAccHostListAdminx)
        order_res = tables.get_orderby(request, unacc_obj_list, adminx.UnAccHostListAdminx)

        # print('----->',order_res)
        paginator = Paginator(order_res[0], adminx.UnAccHostListAdminx.list_per_page)

        page = request.GET.get('page')
        try:
            unacc_objs = paginator.page(page)
        except PageNotAnInteger:
            unacc_objs = paginator.page(1)
        except EmptyPage:
            unacc_objs = paginator.page(paginator.num_pages)

        table_obj = tables.TableHandler(request,
                                        models.UnAccHostList,
                                        adminx.UnAccHostListAdminx,
                                        unacc_objs,
                                        order_res
                                        )
        return render(request, 'salt_unacc_minion.html', {'table_obj': table_obj,
                                               'paginator': paginator})

class ErrMinionListView(LoginRequiredMixin,View):
    def get(self,request):
        err_obj_list = ErrorHostList.objects.filter(key_tag='error')
        # asset_obj_list = models.Asset.objects.all()
        order_res_list = tables.get_orderby(request, err_obj_list, ErrorHostListAdminx)
        order_res = tables.get_orderby(request, err_obj_list, ErrorHostListAdminx)

        # print('----->',order_res)
        paginator = Paginator(order_res[0], ErrorHostListAdminx.list_per_page)

        page = request.GET.get('page')
        try:
            unacc_objs = paginator.page(page)
        except PageNotAnInteger:
            unacc_objs = paginator.page(1)
        except EmptyPage:
            unacc_objs = paginator.page(paginator.num_pages)

        table_obj = tables.TableHandler(request,
                                        ErrorHostList,
                                        ErrorHostListAdminx,
                                        unacc_objs,
                                        order_res
                                        )
        return render(request, 'salt_error_minion.html', {'table_obj': table_obj,
                                               'paginator': paginator})

class AcceptUnaccView(LoginRequiredMixin,View):
   def get(self,request):
       return render(request,'index.html')


class MinionGroupsView(LoginRequiredMixin, View):
    def get(self, request):
        all_minions = AccHostList.objects.all()
        groups = MinionGroups.objects.all()
        return render(request, 'minionGroups.html',{
            'groups':groups,
            'all_minions': all_minions
        })
    def post(self,request):
        groups = MinionGroups.objects.all()
        all_minions = AccHostList.objects.all()
        new_group = CreateGroupsForm(request.POST)
        if new_group.is_valid():
            new_group_name = request.POST.get("creategroups","")
            all_groups = MinionGroups.objects.all()
            all_groups_name = []
            for groups in all_groups:
                all_groups_name.append(groups.Group)
            if new_group_name in all_groups_name:
                msg = ": group已存在，请重新命名！"
                return render(request,'minionGroups.html',{
                    'new_group':new_group,
                    'msg':msg,
                    'all_minions':all_minions
                })
            else:
                msg = ": 创建成功！"
                create_group = MinionGroups
                create_group.objects.create(Group=new_group_name)
                return render(request,'minionGroups.html',{
                    'new_group':new_group,
                    'msg':msg,
                    'all_minions':all_minions
                })
        else:
            from django.core.urlresolvers import reverse
            return HttpResponseRedirect(reverse('hostlist:minion_groups'))

class MinionToGroupView(LoginRequiredMixin,View):
    def post(self,request):
        all_minions = AccHostList.objects.all()
        all_groups = MinionGroups.objects.all()
        miniontogroup = MinionToGroupForm(request.POST)
        if miniontogroup.is_valid():
            addminions = request.POST.getlist('addminions','')
            togroup = request.POST.get('togroup','')
        print all_minions
        return render(request,'minionGroups.html',{
            'all_minions':all_minions,
            'all_groups':all_groups,
                })