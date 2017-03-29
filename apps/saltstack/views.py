#_*_encoding:utf-8_*_
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import  ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from users.utils.mixin_utils import LoginRequiredMixin
from hostlist.models import AccHostList,MinionGroups
from .forms import MinionCmdForm
from scripts.script.saltcmd import saltcommands
import json
#RemoteExecuteView,DeployProgramView,UpdateConfigView,RoutineMaintenanceView,RemoteExecuteApiView,DeployProgramApiView
# Create your views here.
class SaltDeployView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'salt_deploy.html')
class SaltExecuteView(View):
    def get(self,request):
        all_acc_minion = AccHostList.objects.all()
        all_groups = MinionGroups.objects.all()
        return render(request,'salt_excute.html',{
            'all_acc_minion': all_acc_minion,
            'all_groups': all_groups,
        })
    def post(self,request):
        all_acc_minion = AccHostList.objects.all()
        minioncmd_form = MinionCmdForm(request.POST)
        all_groups = MinionGroups.objects.all()
        all_minionid = []
        if minioncmd_form.is_valid():
            minionid = request.POST.getlist("minions", "")
            cmd = request.POST.get("cmd", "")
            groups = request.POST.getlist("groups",'')
            if minionid == '':
                if groups == '':
                    result = 'must input a minion'
                else:
                    for group in groups:
                        Group_que = MinionGroups.objects.get(Group=str(group))
                        group_que_id = Group_que.id
                        Group = MinionGroups.objects.get(id=group_que_id)
                        for minion in Group.minion.all():
                            all_minionid.append(str(minion.minionid))
                    result = saltcommands(all_minionid,cmd)
            else:
                if groups == '':
                    all_minionid = minionid
                    result = saltcommands(all_minionid, cmd)
                else:
                    for group in groups:
                        Group_que = MinionGroups.objects.get(Group=str(group))
                        group_que_id = Group_que.id
                        Group = MinionGroups.objects.get(id=group_que_id)
                        all_minionid = []
                        for minion in Group.minion.all():
                            all_minionid.append(str(minion.minionid))
                            all_minionid = list(set(all_minionid) | set(minionid))
                    result = saltcommands(all_minionid,cmd)
            return render(request, 'salt_excute.html', {
                'all_acc_minion': all_acc_minion,
                'all_groups': all_groups,
                'result':result,
            })
        else:
            return render(request, 'salt_excute.html', {
                'all_acc_minion': all_acc_minion,
                'minioncmd_form':minioncmd_form,
                'all_groups': all_groups,
            })
