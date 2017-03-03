#_*_coding:utf-8_*_
from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    #required字段判断字段是否为空，如果为空，则报错
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=5)