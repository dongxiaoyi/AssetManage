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
from users.utils.mixin_utils import LoginRequiredMixin
import json
import time,subprocess
from .models import OperateRecord


# Create your views here.

class UserRecordView(LoginRequiredMixin,View):
    def get(self,request):
        all_record = OperateRecord.objects.order_by('-id')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_record, 25, request=request)

        records = p.page(page)
        return render(request,'record.html',{'records':records,
                                             })


class GetAllRecordView(LoginRequiredMixin,View):
    def post(self,request):
        record_id = request.POST.get('record','')
        print record_id
        record = OperateRecord.objects.get(id=int(str(record_id)))
        print record
        return render(request,'record_all.html',{'record':record,
                                                 })