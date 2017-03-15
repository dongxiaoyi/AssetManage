# _*_encoding:utf-8_*_
from django.conf.urls import url, include
from django.views.generic import TemplateView
from views import SaltDeployView,SaltExecuteView
#from .views import RemoteExecuteView,DeployProgramView,UpdateConfigView,RoutineMaintenanceView,RemoteExecuteApiView,DeployProgramApiView
urlpatterns = [
    #url(r'^list/$', OrgView.as_view(), name="org_list"),
    url(r'salt_deploy/$',  SaltDeployView.as_view(), name='salt_deploy'),
    url(r'^excute/$',SaltExecuteView.as_view(), name='salt_excute'),


]