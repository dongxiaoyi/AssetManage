#_*_coding:utf-8_*_
from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.models import User

class MinionCmdForm(forms.Form):
    cmd = forms.CharField(required=True,min_length=1)


