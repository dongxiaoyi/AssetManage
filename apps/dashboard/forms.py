#_*_coding:utf-8_*_
from django import forms

class InfoMinionidForm(forms.Form):
    infominionid = forms.CharField(required=True,min_length=1)