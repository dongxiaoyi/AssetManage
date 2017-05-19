# _*_encoding:utf-8_*_
from django.conf.urls import url
from django.views.generic import TemplateView
from .views import UserInfoView,ImageUploadView,UpdatePwdView,SendEmailCodeView,UpdateEmailView,ForgetPwdView
from .views import MyMessagesView,ResetView,ModifyPwdView
urlpatterns = [
    #用户信息
    url(r'^info/$', UserInfoView.as_view(), name="user_info"),

    # 用户头像上传
    url(r'^image-upload/$', ImageUploadView.as_view(), name="image_upload"),

    # 用户个人中心修改密码
    url(r'^update-password/$', UpdatePwdView.as_view(), name="update-password"),

    # 发送邮箱验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name="sendemail_code"),

    # 修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name="update_email"),

    # 我的消息
    url(r'^mymessages/$', MyMessagesView.as_view(), name="mymessages"),
    # 登录界面忘记密码url
    url('^forget_pwd/$', ForgetPwdView.as_view(), name="forget_pwd"),
    #重置密码的链接
    url('^reset/(?P<reset_code>.*)/$', ResetView.as_view(), name="reset_pwd"),
    #重置密码操作
    url('^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),

]