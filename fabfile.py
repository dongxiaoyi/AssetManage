# -*- coding: utf-8 -*-
# 文件名要保存为 fabfile.py

from __future__ import unicode_literals
from fabric.api import *

# 登录用户和主机名：
env.user = 'root'
# 如果没有设置，在需要登录的时候，fabric 会提示输入
env.password = 'sk927312*'
# 如果有多个主机，fabric会自动依次部署
env.hosts = ['salt-master',]

TAR_FILE_NAME = 'deploy-assetmanage-v1.0.tar.gz'


def pack():
    """
    定义一个pack任务, 打一个tar包
    :return:
    """
    tar_files = ['*.py','*.md', 'AssetManage/*.py','script/uwsgi_params','script/uwsgi.ini','script/django_asset.conf','apps/addfields/*.py','apps/asset/*.py','apps/celerys/*.py','apps/dashboard/*.py','apps/fileupload/*.py','apps/hostlist/*.py','record/*.py','saltstack/*.py','scripts/*.py','apps/scripts/script/*.py','apps/users/*.py','extra_apps/xadmin/.tx/*','extra_apps/xadmin/locale/*','extra_apps/xadmin/plugins/*','extra_apps/xadmin/templates/*','extra_apps/xadmin/templatetags/*','extra_apps/xadmin/views/*.py','media/*','templates/*','static/*','requirements.txt']
    exclude_files = ['fabfile.py', 'deploy/*', '*.tar.gz', '.DS_Store', '*/.DS_Store',
                     '*/.*.py', '__pycache__/*']
    exclude_files = ['fabfile.py', 'deploy/*', '*.tar.gz']
    exclude_files = ['--exclude=\'%s\'' % t for t in exclude_files]

    local('mv %s %s_bak' % (TAR_FILE_NAME,TAR_FILE_NAME))
    local('rm -f %s_bak' % TAR_FILE_NAME)
    local('tar -cvzf %s %s %s' % (TAR_FILE_NAME, ' '.join(exclude_files), ' '.join(tar_files)))
    print('在当前目录创建一个打包文件: %s' % TAR_FILE_NAME)


def deploy():
    """
    定义一个部署任务
    :return:
    """
    # 先进行打包
    pack()

    # 远程服务器的临时文件
    remote_tmp_tar = '/tmp/%s' % TAR_FILE_NAME
    run('rm -f %s' % remote_tmp_tar)
    # 上传tar文件至远程服务器, local_path, remote_path
    put(TAR_FILE_NAME, remote_tmp_tar)
    # 解压
    remote_dist_base_dir = '/data/projects/release/v1'
    # 如果不存在, 则创建文件夹
    run('mkdir -p %s' % remote_dist_dir)

    # cd 命令将远程主机的工作目录切换到指定目录
    with cd(remote_dist_dir):
        print('解压文件到到目录: %s' % remote_dist_dir)
        run('tar -xzvf %s' % remote_tmp_tar)
        print('安装 requirements.txt 中的依赖包')
        # 我使用的是 python2.7环境 来开发
        run('pip install -r requirements.txt')
        nginx_file = 'script/django_asset.conf'
        remote_nginx_file = '/etc/nginx/conf.d/django_asset.conf'
        print('上传 nginx 配置文件 %s' % nginx_file)
        put(nginx_file, remote_nginx_file)
        #print('上传uwsgi.ini')
        #uwsgi_ini_file = 'script/uwsgi.ini'
        #remote_uwsgi_ini_file = '/etc/nginx/conf.d/uwsgi.ini'
        #print('上传 uwsgi.ini 配置文件 %s' % uwsgi_ini_file)
        #put(uwsgi_ini_file, remote_uwsgi_ini_file)
        #print('上传uwsgi_params')
        #uwsgi_params_file = 'script/uwsgi_params'
        #remote_uwsgi_params_file = '/etc/nginx/conf.d/uwsgi_params'
        #print('上传 uwsgi_params 配置文件 %s' % uwsgi_params_file)
        #put(uwsgi_params_file, remote_uwsgi_params_file)

        # 在当前目录的子目录 deploy 中的 supervisor 配置文件上传至服务器
    #supervisor_file = 'deploy/django_app.ini'
    #remote_supervisor_file = '/etc/supervisord.d/django_app.ini'
    #print('上传 supervisor 配置文件 %s' % supervisor_file)
    #put(supervisor_file, remote_supervisor_file)

    # 重新加载 nginx 的配置文件
    run('nginx -t')
    run('nginx -s reload')
    # 删除本地的打包文件
    local('rm -f %s' % TAR_FILE_NAME)
    # 载入最新的配置文件，停止原有进程并按新的配置启动所有进程
    #run('supervisorctl reload')
    # 执行 restart all，start 或者 stop fabric 都会提示错误，然后中止运行
    # 但是服务器上查看日志，supervisor 有重启
    # run('supervisorctl restart all')