# _*_encoding:utf-8_*_
from django.conf.urls import url, include
from django.views.generic import TemplateView
from views import SaltDeployDevView,SaltExecuteView,PullDevServicesView,UpdateDevServiceView,PullDevServicesTestView
#from .views import RemoteExecuteView,DeployProgramView,UpdateConfigView,RoutineMaintenanceView,RemoteExecuteApiView,DeployProgramApiView
urlpatterns = [
    #url(r'^list/$', OrgView.as_view(), name="org_list"),
    url(r'salt_deploy_dev/$',  SaltDeployDevView.as_view(), name='salt_deploy_dev'),
    url(r'^excute/$',SaltExecuteView.as_view(), name='salt_excute'),
    url(r'^pull/dev/services/$', PullDevServicesView.as_view(), name='pulldevservices'),
    url(r'^pull/dev/services/test$', PullDevServicesTestView.as_view(), name='pulldevservicestest'),

    #更新开发环境的服务配置
    url(r'^update/dev/service/$', UpdateDevServiceView.as_view(), name='update_dev_service'),

]