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


class PullDevServicesTestForm(forms.Form):
    pulldevservicestestnames = forms.CharField(required=True,max_length=255)
    pulldevtestminions = forms.CharField(required=False)
    pulldevtestfile = forms.CharField(required=True, max_length=255)


class PullservicesnamesForm(forms.Form):
    pulldevservicesnames = forms.CharField(required=True, max_length=255)