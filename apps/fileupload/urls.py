# _*_encoding:utf-8_*_
from django.conf.urls import url, include
from django.views.generic import TemplateView
from views import  UploadView, UploadJoinView,UploadRemoveView,UploadGitView,UploadDownloadView
#from .views import RemoteExecuteView,DeployProgramView,UpdateConfigView,RoutineMaintenanceView,RemoteExecuteApiView,DeployProgramApiView
urlpatterns = [
    #url(r'^list/$', OrgView.as_view(), name="org_list"),
    url(r'upload/$',  UploadView.as_view(), name='upload'),
    url(r'upload/git/$', UploadGitView.as_view(), name='upload_git'),
    url(r'upload/join/(?P<id_code>.*)/$', UploadJoinView.as_view(), name='upload_join'),
    url(r'upload/remove/$', UploadRemoveView.as_view(), name='upload_remove'),
    url(r'upload/download/$', UploadDownloadView.as_view(), name='upload_download'),

]