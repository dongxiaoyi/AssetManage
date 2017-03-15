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
from hostlist.models import AccHostList
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
        return render(request,'salt_excute.html',{
            'all_acc_minion': all_acc_minion,
        })
    def post(self,request):
        all_acc_minion = AccHostList.objects.all()
        minioncmd_form = MinionCmdForm(request.POST)
        if minioncmd_form.is_valid():
            minionid = request.POST.getlist("minions", "")
            cmd = request.POST.get("cmd", "")
            result = saltcommands(minionid,cmd)
            return render(request, 'salt_excute.html', {
                'all_acc_minion': all_acc_minion,
                'result':result
            })
        else:
            return render(request, 'salt_excute.html', {
                'all_acc_minion': all_acc_minion,
                'minioncmd_form':minioncmd_form,
            })
