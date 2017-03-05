#_*_encoding:utf-8_*_
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import  ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from forms import ForgetForm,ModifyPwdForm,UploadImageForm,UserInfoForm
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_email
from models import EmaliVerifyRecord
from .utils.mixin_utils import LoginRequiredMixin
from .models import UserMessage
from .forms import UploadImageForm,UserInfoForm,ModifyPwdForm,ForgetForm
import json

class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class UserInfoView(LoginRequiredMixin,View):
    '''个人用户信息'''
    def get(self,request):
        return render(request,'usercenter-info.html',{
        })
    def post(self,request):
        user_info_form = UserInfoForm(request.POST,instance=request.user)
        print user_info_form
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success","msg":"修改成功"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')

class ForgetPwdView(View):
    def get(self,request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html',{'forget_form':forget_form})
    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email','')
            send_register_email(email, "forget")
            return render(request,'send_success.html')
        else:
            return render(request, 'forgetpwd.html',{'forget_form':forget_form})



class ResetView(View):
    def get(self,request,reset_code):
        all_records = EmaliVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request,'password_reset.html',{'email':email})
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')

class ModifyPwdView(View):
    '''
    修改用户密码
    '''
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get('email','')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email,'msg':'密码不一致'})
            else:
                user = User.objects.get(email=email)
                user.password = make_password(pwd2)
                user.save()
                return render(request, 'modify_success.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html',{'email':email,'modify_form':modify_form})


class ImageUploadView(LoginRequiredMixin,View):
    '''
    用户修改头像
    '''
    def post(self,request):
        image_form = UploadImageForm(request.POST,request.FILES,instance=request.user)
        if image_form.is_valid():
            request.user.save()
            return HttpResponse('{"status":"success","msg":"修改成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"修改失败"}', content_type='application/json')


class UpdatePwdView(LoginRequiredMixin,View):
    '''
    在个人中心修改密码
    '''
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            else:
                user = request.user
                user.password = make_password(pwd2)
                user.save()
                return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin,View):
    '''
    发送邮箱验证码
    '''
    def get(self,request):
        email = request.GET.get('email','')
        print email
        if User.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')
        print 'test'
        send_register_email(email,'up_email')
        print 'success'
        return HttpResponse('{"status":"success"}', content_type='application/json')

class UpdateEmailView(LoginRequiredMixin,View):
    '''
    修改个人邮箱
    '''
    def post(self,request):
        email = request.POST.get('email','')
        code = request.POST.get('code','')

        existed_record = EmaliVerifyRecord.objects.filter(email=email,code=code,send_type='up_email')
        if existed_record:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')

class MyMessagesView(LoginRequiredMixin,View):
    '''
    我的消息
    '''
    def get(self,request):
        all_messages = UserMessage.objects.filter(user=request.user)

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_messages, 5, request=request)

        messages = p.page(page)
        for message in all_messages:
            print message.has_read
            if message.has_read == False:
                message.has_read = True
                message.save()
                print message.has_read
        unread_num = 0
        return render(request,'usercenter-message.html',{
            'all_messages':messages,
            'unread_num':unread_num,
        })

class ResetView(View):
    def get(self,request,reset_code):
        all_records = EmaliVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request,'password_reset.html',{'email':email})
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html',{})
    response.status_code = 404
    return response


def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html',{})
    response.status_code = 500
    return response