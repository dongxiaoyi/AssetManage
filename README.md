# AssetManage
1.客户端传到的服务端的数据格式类似：
{'asset_data': '{"asset_id": null, "wake_up_type": "Power Switch", "uuid": "67AC7301-54C0-11CB-9ED5-968C3BA3A0AD", "os_release": "Ubuntu 16.10", "os_type": "linux", "cpu_count": "4", "ram": [{"slot": "ChannelA-DIMM0", "capacity": "8192", "manufactory": "Samsung", "asset_tag": "None", "sn": "00122211", "model": "DDR3"}], "cpu_model": "Intel(R) Core(TM) i5-5200U CPU @ 2.20GHz", "manufactory": "LENOVO", "physical_disk_driver": [], "sn": "PF0H1JDB", "cpu_core_count": "8", "nic": [], "model": "20DCA088CD", "os_distribution": "Ubuntu", "asset_type": "server", "ram_size": 7719}'}
问题：
临时存放这些数据的“新上线待批准资产”的表可以和真正批准后存放的资产表一样类似的建立多个完整存放这些数据的表，但是新上线待批准资产是总表，它关联其他的表,
目前是存放在一张表中，数据不完整，新增的待批准资产方法core.save_new_asset_to_approval_zone中,这个方法可以多加几个用来存放比如ram，disk的数据，但是要
写在总表后，用来关联总表，方便在批准时一块提交（批准的view为NewAssetApprovalView,可以在其中修改具体存放到数据库的数据）.
2.问题：
目前“新上线待批准资产”保存形式未按照客户端上传字段保存，后期会修改代码，否则无法批准后保存客户端上传的完整信息，只能手工填写！
3.问题：
资产更新：core.data_inject中的update_asset,厂商字段注释掉了，目前server可以更新ram，disk，nic,cpu,server;但是server的更新是因为update的asset_type是server，如果是网络设备等还没有做！
4.问题：
ubuntu等其他设备的网卡信息抓取有区别，目前没做，raid信息目前也因为设备和抓取工具的问题需要另行增加判断和实现。
5.事件变更记录尚未实现
EventLog有点问题，再行实现吧！
所以，前端页面的事件变更是不能显示的！
6.增加注册及忘记密码功能：
注册邮件发送给管理员，由管理员验证（注册表带验证码功能）
忘记密码的重置链接发送给管理员，由管理员给用户重置操作的链接（涉及code必须隐秘）
7.增加个人中心，可以修改密码,头像，个人信息及查看messages
8.messages功能添加
9.未读计数功能
10.集成saltstack（未完成）
11.分类视图功能注释掉了，因为还没有做，相关资产的配置和配置权限也没有做！
12.404+500页面：
    需要DEBUG模式可以：
        1.settings.py
            注释掉STATIC_ROOT
            修改为ALLOWED_HOSTS = ['*']
            修改为DEBUG = True
        2.urls.py
            注释掉from .settings import STATIC_ROOT
            注释掉url('^static/(?P<path>.*)', serve, {'document_root': STATIC_ROOT}),
            注释掉handler404 = 'users.views.page_not_found'和handler500 = 'users.views.page_error'

！！！用户名必须和邮件一致，否则重置密码会有问题，需要添加昵称的话需要在migrate之前加到MyUser这个model，否则一旦生成表结构就无法添加字段