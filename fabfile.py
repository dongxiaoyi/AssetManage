#from __future__ import unicode_literals
# -*- coding: utf-8 -*-
# 文件名要保存为 fabfile.py
from sys import argv
from fabric.api import *

# 登录用户和主机名：
env.user = 'root'
# 如果没有设置，在需要登录的时候，fabric 会提示输入
env.password = 'sk927312*'
# 如果有多个主机，fabric会自动依次部署
env.hosts = ['salt-master',]
#定义分组
env.roledefs = {'web':['192.168.0.4',],'db':['192.168.0.4','192.168.0.5']}

version = 'v1.0'

TAR_FILE_NAME = 'deploy-assetmanage-' + version + '.tar.gz'

@task
@runs_once
def pack():
    """
    定义一个pack任务, 打一个tar包
    :return:
    """
    git_version = version
    lcd('/data/projects/')
    git_menu = '/data/projects/git/'
    exclude_files = ['%s%s/fabfile.py' % (git_menu,git_version),
                     '%s%s/AssetManageClient' % (git_menu, git_version),
                     '%s%s/apps/addfields/migrations' % (git_menu, git_version),
                     '%s%s/apps/asset/migrations' % (git_menu, git_version),
                     '%s%s/apps/dashboard/migrations' % (git_menu, git_version),
                     '%s%s/apps/fileupload/migrations' % (git_menu, git_version),
                     '%s%s/apps/record/migrations' % (git_menu, git_version),
                     '%s%s/apps/saltstack/migrations' % (git_menu, git_version),
                     '%s%s/extra_apps/xadmin/migrations' % (git_menu, git_version),
                    ]
    exclude_files = ['--exclude=\'%s\'' % t for t in exclude_files]

    local('rm -f /data/projects/tar/%s_bak' % TAR_FILE_NAME)
    local('tar -cvzf %s %s -C /data/projects/git/ %s' % ('/data/projects/tar/' + TAR_FILE_NAME, ' '.join(exclude_files), version))
    print('在当前目录创建一个打包文件: %s' % TAR_FILE_NAME)

@task
@roles('web')
def deploy():
    """
    定义一个部署任务
    :return:
    """
    get_tar = '/data/projects/tar/%s' % TAR_FILE_NAME
    run('rm -f %s' % get_tar)
    # 上传tar文件至远程服务器, local_path, remote_path
    put('/data/projects/tar/' + TAR_FILE_NAME, '/data/projects/tar/')
    # cd 命令将远程主机的工作目录切换到指定目录
    remote_dist_dir = '/data/projects/html/'
    with cd(remote_dist_dir):
        print('解压文件到到目录: %s' % remote_dist_dir)
        run('tar -xzvf %s -C %s' % (get_tar,remote_dist_dir))
        print('安装 requirements.txt 中的依赖包')
        # 我使用的是 python2.7环境 来开发
        run('pip install -r /data/projects/html/%s/requirements.txt' % version)
        nginx_file = ('/data/projects/html/%s/script/nginx_asset.conf' % version)
        remote_nginx_file = '/etc/nginx/conf.d/django_asset.conf'
        print('复制 nginx 配置文件 %s' % nginx_file)
        run('/usr/bin/cp %s %s' % (nginx_file, remote_nginx_file))
    # 重新加载 nginx 的配置文件
    run('nginx -t && nginx -s reload')
    # 删除本地的打包文件
    local('rm -f %s' % TAR_FILE_NAME)
