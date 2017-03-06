# _*_encoding:utf-8_*_
from django.conf.urls import url, include
from django.views.generic import TemplateView
from views import BaseView
#from .views import RemoteExecuteView,DeployProgramView,UpdateConfigView,RoutineMaintenanceView,RemoteExecuteApiView,DeployProgramApiView
urlpatterns = [
    #url(r'^list/$', OrgView.as_view(), name="org_list"),
    url(r'base/$',  BaseView.as_view(), name='base'),
    #url(r'^execute/$',RemoteExecuteView.as_view(), name='execute'),
    #url(r'^deploy/$', DeployProgramViewas_view(), name='deploy'),
    #url(r'^update/$', UpdateConfigViewas_view(), name='update'),
    #url(r'^routine/$', RoutineMaintenanceViewas_view(), name='routine'),
    #url(r'^api/execute/$', RemoteExecuteApiViewas_view(), name='execute_api'),
    #url(r'^api/deploy/$', DeployProgramApiViewas_view(), name='deploy_api'),

]