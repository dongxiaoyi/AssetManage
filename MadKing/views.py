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
from forms import LoginForm


class IndexView(View):
    '''
    首页
    '''
    def get(self,request):
        return render(request,'index.html',{
        })


class AccLoginView(View):
    '''
    用户登录
    '''
    def get(self,request):
        return render(request, 'login.html')
    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    from django.core.urlresolvers import reverse
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': "用户未激活"})
            else:
                return render(request, 'login.html', {'msg': "用户名或者密码错误"})
        else:
            return render(request, 'login.html',{'login_form':login_form})

class AccLogoutView(View):
    '''
    用户登出
    '''
    def get(self,request):
        logout(request)
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse('login'))

