#_*_coding:utf-8_*_
from django import forms
#from hostlist.models import *
#
#class HostsListForm(forms.ModelForm):
#    class Meta:
#        model = HostList
#        widgets = {
#          'hostname': forms.TextInput(attrs={'class': 'form-control'}),
#          'ip': forms.TextInput(attrs={'class': 'form-control'}),
#          'catagory': forms.TextInput(attrs={'class': 'form-control'}),
#          'dccn': forms.TextInput(attrs={'class': 'form-control'}),
#          'engineer': forms.TextInput(attrs={'class': 'form-control'}),
#          'macaddr': forms.TextInput(attrs={'class': 'form-control'}),
#          'zsourceip': forms.TextInput(attrs={'class': 'form-control'}),
#          'bsourceip': forms.TextInput(attrs={'class': 'form-control'}),
#          'licdate': forms.TextInput(attrs={'class': 'form-control'}),
#          'licstatus': forms.TextInput(attrs={'class': 'form-control'}),
#          'remark': forms.TextInput(attrs={'class': 'form-control'}),
#        }
#
class CreateGroupsForm(forms.Form):
    creategroups = forms.CharField(required=True,min_length=1)

#class MinionToGroupForm(forms.Form):
#    oldminions = forms.CharField(required=True,min_length=0)
#    newminions = forms.CharField(required=True,min_length=0)
#    togroup = forms.CharField(required=True,min_length=1)