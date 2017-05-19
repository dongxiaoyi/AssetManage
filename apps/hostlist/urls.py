# _*_encoding:utf-8_*_
from django.conf.urls import url, include
from django.views.generic import TemplateView
#from views import BaseView
from .views import AccMinionListView,UnAccMinionListView,ErrMinionListView,AcceptUnaccView,MinionGroupsView
#from .views import MinionToGroupView
from .views import GroupAddMinionsView,DeleteGroupView
urlpatterns = [
    url(r'^acc_minion_list/$', AccMinionListView.as_view(), name="acc_minion_list"),
    url(r'^unacc_minion_list/$', UnAccMinionListView.as_view(), name="unacc_minion_list"),
    url(r'^error_minion_list/$', ErrMinionListView.as_view(), name="error_minion_list"),
    #操作unaccept的minion通过验证
    url(r'^accept_unacc/$', AcceptUnaccView.as_view(), name="accept_unacc"),
    url(r'^minion_groups/$', MinionGroupsView.as_view(), name="minion_groups"),
    #url(r'^minion_to_group/$', MinionToGroupView.as_view(), name="minion_to_group"),
    url('minion_to_group/(?P<group_id>.*)/$', GroupAddMinionsView.as_view(), name="group_add_minions"),
    url(r'^delete_group/$', DeleteGroupView.as_view(), name="delete_group"),

]