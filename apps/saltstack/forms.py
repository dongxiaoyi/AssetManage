#_*_coding:utf-8_*_
from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.models import User

class MinionCmdForm(forms.Form):
    cmd = forms.CharField(required=True,min_length=1)

class DevServiceForm(forms.Form):
    servicename = forms.CharField(max_length=255)
    sls = forms.Textarea()


class UpdateDevServiceForm(forms.Form):
    updatedevservicename = forms.CharField(required=True,max_length=255)
    updatedevminions = forms.CharField(required=False)
    updatedevgroups =  forms.CharField(required=False)
    updatedevfilename = forms.CharField(required=True,max_length=255)
    updatedevsls = forms.Textarea()


class PullDevServiceForm(forms.Form):
    pulldevservicename = forms.CharField(required=True,max_length=255)
    pulldevminions = forms.CharField(required=False)
    pulldevgroups = forms.CharField(required=False)
    pulldevfile = forms.CharField(required=True, max_length=255)


class PullservicesnamesForm(forms.Form):
    pulldevservicesnames = forms.CharField(required=True, max_length=255)