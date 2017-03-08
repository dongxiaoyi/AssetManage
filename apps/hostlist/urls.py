# _*_encoding:utf-8_*_
from django.conf.urls import url, include
from django.views.generic import TemplateView
#from views import BaseView
from .views import AccMinionListView,UnAccMinionListView,RejMinionListView,AcceptUnaccView
urlpatterns = [
    url(r'^acc_minion_list/$', AccMinionListView.as_view(), name="acc_minion_list"),
    url(r'^unacc_minion_list/$', UnAccMinionListView.as_view(), name="unacc_minion_list"),
    url(r'^rej_minion_list/$', RejMinionListView.as_view(), name="rej_minion_list"),
    #操作unaccept的minion通过验证
    url(r'^accept_unacc/$', AcceptUnaccView.as_view(), name="accept_unacc"),
    #url(r'base/$',  BaseView.as_view(), name='base'),
    #url(r'^execute/$',RemoteExecuteView.as_view(), name='execute'),
    #url(r'^deploy/$', DeployProgramViewas_view(), name='deploy'),
    #url(r'^update/$', UpdateConfigViewas_view(), name='update'),
    #url(r'^routine/$', RoutineMaintenanceViewas_view(), name='routine'),
    #url(r'^api/execute/$', RemoteExecuteApiViewas_view(), name='execute_api'),
    #url(r'^api/deploy/$', DeployProgramApiViewas_view(), name='deploy_api'),

]