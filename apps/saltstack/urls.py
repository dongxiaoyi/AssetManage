# _*_encoding:utf-8_*_
from django.conf.urls import url, include
from django.views.generic import TemplateView
from views import SaltDeployDevView,SaltExecuteView,PullDevServicesView,UpdateDevServiceView,PullDevServicesTestView,PullDevServiceView,PullDevServicesAllTestView
from views import DevServiceDeleteView
#from .views import RemoteExecuteView,DeployProgramView,UpdateConfigView,RoutineMaintenanceView,RemoteExecuteApiView,DeployProgramApiView
urlpatterns = [
    #url(r'^list/$', OrgView.as_view(), name="org_list"),
    #服务上传界面
    url(r'salt_deploy_dev/$',  SaltDeployDevView.as_view(), name='salt_deploy_dev'),
    url(r'^excute/$',SaltExecuteView.as_view(), name='salt_excute'),
    url(r'^pull/dev/service/$', PullDevServiceView.as_view(), name='pulldevservice'),
    url(r'^pull/dev/services/$', PullDevServicesView.as_view(), name='pulldevservices'),
    url(r'^pull/dev/services/test/$', PullDevServicesTestView.as_view(), name='pulldevservicestest'),
    url(r'^pull/dev/services/alltest/$', PullDevServicesAllTestView.as_view(), name='pulldevservicesalltest'),
    #删除服务
    url(r'^dev/service/delete/$', DevServiceDeleteView.as_view(), name='devservicedelete'),

    #更新开发环境的服务配置
    url(r'^update/dev/service/$', UpdateDevServiceView.as_view(), name='update_dev_service'),

]