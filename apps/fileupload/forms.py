#_*_coding:utf-8_*_
from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.models import User

class UploadFilesForm(forms.Form):
    filesource = forms.FileField()
    #filename = forms.CharField()