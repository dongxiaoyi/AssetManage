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
from hostlist.models import AccHostList,UnAccHostList,ErrorHostList
from dashboard.models import MasterLoadAvg,MasterProcessStatus,MinionOnlineNumber
from weblog.models import PvModel,UvModel,IvModel
import datetime

class IndexView(LoginRequiredMixin,View):
    '''
    首页
    '''
    def get(self,request):
        now_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        all_acc_minions = AccHostList.objects.all()
        all_unacc_minons = UnAccHostList.objects.all()
        all_error_minions = ErrorHostList.objects.all()
        '''master负载'''
        master_loadavg_query_list = MasterLoadAvg.objects.all()
        master_loadavg_list = []
        for loadavg in master_loadavg_query_list:
            master_loadavg_list.append(loadavg)
        loadavg = master_loadavg_list[-1]
        '''内存信息()'''
        mem = {}
        sys_version_command = str('uname -a|grep -i ubuntu|wc -l')
        sys_version = subprocess.Popen(sys_version_command, stdout=subprocess.PIPE, shell=True)
        sys_version_stdout =sys_version.communicate()[0]
        if int(sys_version_stdout) == int(1):
            mem = {}
        else:
            mem_command = 'free -m|head -3|tail -2'
            mems = subprocess.Popen(mem_command, stdout=subprocess.PIPE, shell=True)
            mem_stdout = mems.communicate()[0]
            print mem_stdout
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
                mem['mem_used: '] = str(mem_used)
            for mem_free in mem_used_free_list[-1:]:
                mem['mem_free: '] = str(mem_free)
            swap_used_free_line = mem_info_list[2]
            swap_used_free_list = []
            for swap_used_free in swap_used_free_line.strip('\n').split('        '):
                swap_used_free_list.append(str(swap_used_free))
            for swap_used in swap_used_free_list[-2:-1]:
                mem['swap_used: '] = str(swap_used)
            for swap_free in mem_used_free_list[-1:]:
                mem['swap_free: '] = str(swap_free)
        '''进程状态'''
        master_status_query_all = MasterProcessStatus.objects.all()
        master_query_status_list = []
        for master_status_query in master_status_query_all:
            master_query_status_list.append(master_status_query)
        master_status = master_query_status_list[-1]
        '''minion数量'''
        acc_minions_count = all_acc_minions.count()
        unacc_minions_count = all_unacc_minons.count()
        error_minions_count = all_error_minions.count()
        '''minion在线数量'''
        all_online = MinionOnlineNumber.objects.all()
        online_list = []
        for online_query in all_online:
            online_list.append(online_query)
        online = online_list[-1]
        '''PV,IV,IP数据'''
        now = datetime.datetime.now()
        twodays = now + datetime.timedelta(days=-1)
        threedays = now + datetime.timedelta(days=-2)
        fourdays = now + datetime.timedelta(days=-3)
        fivedays = now + datetime.timedelta(days=-4)
        sixdays = now + datetime.timedelta(days=-5)
        sevendays = now + datetime.timedelta(days=-6)
        one_formatted = now.strftime("%Y-%m-%d")
        two_formatted = twodays.strftime("%Y-%m-%d")
        three_formatted = threedays.strftime("%Y-%m-%d")
        four_formatted = fourdays.strftime("%Y-%m-%d")
        five_formatted = fivedays.strftime("%Y-%m-%d")
        six_formatted = sixdays.strftime("%Y-%m-%d")
        seven_formatted = sevendays.strftime("%Y-%m-%d")
        seven_pv = {}
        seven_uv = {}
        seven_ip = {}
        time_pv_sort = []
        time_uv_sort = []
        time_ip_sort = []
        sort_pv_key = []
        sort_uv_key = []
        sort_ip_key = []
        sortd_pv_key = []
        sortd_uv_key = []
        sortd_ip_key = []
        pv_sort = {}
        uv_sort = {}
        ip_sort = {}

        sevendays_pv = PvModel.objects.filter(timestamps__lte=seven_formatted)
        for pv_query in sevendays_pv:
            pv_num = pv_query.pv
            logname = pv_query.logname
            timstamps = pv_query.timestamps
            pv_sort[timstamps] = pv_num
            for key,value in pv_sort.items():
                sort_pv_key.append(key)
            for key in sorted(sort_pv_key):
                sortd_pv_key.append(pv_sort[key])
            seven_pv[logname] = sortd_pv_key
        sevendays_uv = UvModel.objects.filter(timestamps__lte=seven_formatted)
        for uv_query in sevendays_uv:
            uv_num = uv_query.uv
            logname = uv_query.logname
            timstamps = uv_query.timestamps
            uv_sort[timstamps] = uv_num
            for key,value in uv_sort.items():
                sort_uv_key.append(key)
            for key in sorted(sort_uv_key):
                sortd_uv_key.append(uv_sort[key])
            seven_uv[logname] = sortd_uv_key
        sevendays_iv = IvModel.objects.filter(timestamps__lte=seven_formatted)
        for iv_query in sevendays_pv:
            iv_num = iv_query.pv
            logname = iv_query.logname
            timstamps = iv_query.timestamps
            ip_sort[timstamps] = iv_num
            for key,value in ip_sort.items():
                sort_ip_key.append(key)
            for key in sorted(sort_ip_key):
                sortd_ip_key.append(ip_sort[key])
            seven_ip[logname] = sortd_ip_key
        '''PV,IV,IP图'''
       #from matplotlib.figure import Figure
       #from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
       #import numpy as np
       #import matplotlib.pyplot as plt
       #fig = Figure(1)
       #n_groups = 7

       #fig, ax = plt.subplots()

       #index = np.arange(n_groups)
       #bar_width = 0.35

       #opacity = 0.4
       #error_config = {'ecolor': '0.3'}
       #for log,pv in sevendays_pv:
       #    locals()['pv_%s' % log] = (pv[one_formatted],pv[two_formatted], pv[three_formatted], pv[four_formatted], pv[five_formatted],pv[six_formatted],pv[seven_formatted])
       #    locals()[log] = plt.bar(index, locals()['pv_%s' % log], bar_width,
       #                 alpha=opacity,
       #                 color='b',
       #                 error_kw=error_config,
       #                 label='Men')

       #plt.xlabel(u'时间')
       #plt.ylabel(u'次数')
       #plt.title(u'七天内PV,UV,IP变化')
       #plt.xticks(index + bar_width, (one_formatted, two_formatted, three_formatted, four_formatted, five_formatted,six_formatted,seven_formatted))
       #plt.legend()

       #plt.tight_layout()
       #fig.autofmt_xdate()
       #canvas = FigureCanvas(fig)
       #pv_plt = HttpResponse(content_type='image/png')
       #canvas.print_png(pv_plt)

        return render(request,'index.html',{'now_time':now_time,
                                            'loadavg':loadavg,
                                            'mem':mem,
                                            'master_status':master_status,
                                            'all_acc_minions':all_acc_minions,
                                            'acc_minions_count':acc_minions_count,
                                            'unacc_minions_count':unacc_minions_count,
                                            'error_minions_count':error_minions_count,
                                            'online':online,
                                            'one_formatted':one_formatted,
                                            'two_formatted':two_formatted,
                                            'three_formatted':three_formatted,
                                            'four_formatted':four_formatted,
                                            'five_formatted':five_formatted,
                                            'six_formatted':six_formatted,
                                            'seven_formatted':seven_formatted,
                                            'seven_pv':seven_pv,
                                            'seven_uv':seven_uv,
                                            'seven_ip':seven_ip,
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


