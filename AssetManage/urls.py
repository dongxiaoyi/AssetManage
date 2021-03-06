#_*_encoding:utf-8_*_

from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
import xadmin

from django.views.static import serve
from .settings import MEDIA_ROOT
#配置404需要打开
#from .settings import STATIC_ROOT

from .views import IndexView,AccLoginView,AccLogoutView,RegisterView,ActiveUserView
from dashboard.views import IndexMinionsView

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^xadmin/', xadmin.site.urls),
    #asset相关url
    url(r'^asset/', include('asset.urls', namespace='asset'), ),
    url(r'^salt/', include('saltstack.urls', namespace='salt'), ),
    url(r'^hostlist/', include('hostlist.urls', namespace='hostlist'), ),
    #文件上传相关
    url(r'^fileupload/', include('fileupload.urls', namespace='fileupload'), ),
    url(r'^record/', include('record.urls', namespace='record'), ),

    url('^$', IndexView.as_view(),name="index"),
    url('^indexminions/$', IndexMinionsView.as_view(), name="indexminions"),
    url(r'^login/$', AccLoginView.as_view(), name='login'),
    url(r'^logout/$', AccLogoutView.as_view(), name='logout'),
    url('^register/$', RegisterView.as_view(), name="register"),
    url('^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    #配置上传文件的访问处理函数
    url('^media/(?P<path>.*)', serve,{'document_root':MEDIA_ROOT}),
    # 配置静态资源的访问处理函数,配置404后需要打开
    #url('^static/(?P<path>.*)', serve, {'document_root': STATIC_ROOT}),
    #富文本相关
    url(r'^ueditor/',include('DjangoUeditor.urls' )),
    #rest-framework
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #验证码
    url(r'^captcha/',include('captcha.urls')),
    # 个人中心相关url
    url(r'^users/', include('users.urls', namespace='users'), ),
]

#handler404 = 'users.views.page_not_found'
#handler500 = 'users.views.page_error'