#_*_encoding:utf-8_*_
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import  ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
import time,subprocess
from users.utils.email_send import send_register_email
from AssetManage.settings import EMAIL_HOST_USER
from users.models import UserMessage,EmaliVerifyRecord
from users.utils.mixin_utils import LoginRequiredMixin
from hostlist.models import AccHostList
from .models import MinionLoadAvg
from .forms import InfoMinionidForm


class IndexMinionsView(LoginRequiredMixin,View):
    def post(self,request):
        info_minionid_form = InfoMinionidForm(request.POST)
        if info_minionid_form.is_valid():
            minionid = request.POST.get('infominionid','')
            print minionid
            '''负载'''
            loadavg_query_list = MinionLoadAvg.objects.filter(minionid=str(minionid))
            loadavg_list = []
            for loadavg in loadavg_query_list:
                loadavg_list.append(loadavg)
            loadavg = loadavg_list[-1]
            print loadavg
            return render(request,"index_minions.html",{'loadavg':loadavg,
                                                        })