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
from forms import LoginForm,RegisterForm
from users.utils.email_send import send_register_email
from AssetManage.settings import EMAIL_HOST_USER
from users.models import UserMessage,EmaliVerifyRecord
from users.utils.mixin_utils import LoginRequiredMixin



class IndexView(LoginRequiredMixin,View):
    '''
    首页
    '''
    def get(self,request):
        now_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        '''当前服务器负载'''
        with open('/proc/loadavg','r') as loadavg:
            cpuload = loadavg.readline()
        cpuloads = []
        for load in cpuload.split(' '):
            cpuloads.append(str(load))
        cpuloads = cpuloads
        '''内存信息'''
        mem = {}
        mem_command = 'free -m|head -3|tail -2'
        mems = subprocess.Popen(mem_command, stdout=subprocess.PIPE, shell=True)
        mem_stdout = mems.communicate()[0]
        mem_info_list = []
        for mem_line in mem_stdout.split('\n'):
            mem_info_list.append(str(mem_line))
        buffers_cached_line = mem_info_list[0]
        buffer_cache_list = []
        for buffer_cache in buffers_cached_line.strip('\n').split('        '):
            buffer_cache_list.append(buffer_cache)
        for buffer in buffer_cache_list[-2:-1]:
            mem['buffers: '] = str(buffer)
        for cache in buffer_cache_list[-1:]:
            mem['cached: '] = str(cache)
        trust_mem_used_free_info_line = mem_info_list[1]
        mem_used_free_list = []
        for mem_used_free in trust_mem_used_free_info_line.strip('\n').split('        '):
            mem_used_free_list.append(str(mem_used_free))
        for mem_used in mem_used_free_list[-2:-1]:
            mem['used: '] = str(mem_used)
        for mem_free in mem_used_free_list[-1:]:
            mem['free: '] = str(mem_free)
        print mem
        return render(request,'index.html',{'now_time':now_time,
                                            'cpuloads':cpuloads,
                                            'mem':mem
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

class RegisterView(View):
    '''
    用户注册
    '''

    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if User.objects.filter(email=user_name):
                if User.objects.filter(is_active=True):
                    return render(request, "register.html", {"register_form": register_form, "msg": '用户已存在'})
                elif User.objects.filter(is_active=False):
                    return render(request, "register.html",
                                  {"register_form": register_form, "msg": '用户已存在但未激活，请查收邮件验证后再登录'})
            else:
                pass_word = request.POST.get("password", "")
                user_profile = User()
                user_profile.username = user_name
                user_profile.email = user_name
                user_profile.is_active = False
                user_profile.password = make_password(pass_word)
                user_profile.save()
                # 写入欢迎注册消息
                user_message = UserMessage()
                user_message.user = User.objects.get(email=user_name)
                user_message.message = '欢迎注册AssetManage'
                user_message.save()
                #未读计数
                #unread_num = User.objects.filter(email=user_name)
                #unread_num.un

                send_register_email(user_name, "register")
                return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})

class ActiveUserView(View):
    def get(self,request,active_code):
        all_records = EmaliVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = User.objects.get(email=email)
                user.is_active =True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


