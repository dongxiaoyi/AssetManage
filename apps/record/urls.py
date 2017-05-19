# _*_encoding:utf-8_*_
from django.conf.urls import url, include
from django.views.generic import TemplateView
from .views import UserRecordView,GetAllRecordView



urlpatterns = [
    url(r'^user/record/$', UserRecordView.as_view(), name="user_record"),
    url(r'^user/record/get_all_record/$', GetAllRecordView.as_view(), name="get_all_record"),
]