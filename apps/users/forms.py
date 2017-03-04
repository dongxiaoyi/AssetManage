#_*_coding:utf-8_*_
from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.models import User

class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})

class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True,min_length=5)
    password2 = forms.CharField(required=True,min_length=5)

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['image']

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['gender','mobile']