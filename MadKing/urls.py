#_*_encoding:utf-8_*_

from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
import xadmin
from django.views.static import serve
from settings import MEDIA_ROOT
from .views import IndexView,AccLoginView,AccLogoutView

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    #asset相关url
    url(r'^asset/', include('asset.urls', namespace='asset'), ),
    url('^$', IndexView.as_view(),name="index"),
    url(r'^login/$', AccLoginView.as_view(), name='login'),
    url(r'^logout/$', AccLogoutView.as_view(), name='logout'),
    #配置上传文件的访问处理函数
    url('^media/(?P<path>.*)', serve,{'document_root':MEDIA_ROOT}),
    # 配置静态资源的访问处理函数
    #url('^static/(?P<path>.*)', serve, {'document_root': STATIC_ROOT}),
    #富文本相关
    url(r'^ueditor/',include('DjangoUeditor.urls' )),
    #rest-framework
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
