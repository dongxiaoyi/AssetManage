#!/usr/bin/env python
# --coding:utf8--
'''''
http://www.cnblogs.com/onlyfu/p/4926351.html
'''
from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *
from fabric.contrib.console import confirm
import time

# environment value
env.user = 'root'
env.hosts = ['192.168.0.4', ]
env.password = 'sk927312*'
env.project_dev_source = '/var/www/html/'  # 开发机项目主目录
env.project_tar_source = '/var/www/releases/'  # 开发机压缩包目录
env.project_pack_name = 'release'  # 项目压缩包名release.tar.gz
env.deploy_project_root = '/var/www/html/'  # 生产环境主目录
env.deploy_release_dir = 'releases'  # 项目发布目录:/var/www/html/releases/下
env.deploy_current_dir = 'current'  # 对外服务当前版本软连接
env.deploy_version = time.strftime("%Y%m%d") + "v2"  # 版本号
env.deploy_full_path = ""


# 版本号,回归操作
@runs_once
def input_versionid():
    return prompt("input project roollback version ID:", default="")


# 打包本地项目
@task
@runs_once
def tar_source():
    print yellow("creating source package...")
    with lcd(env.project_dev_source):
        local("tar -zcf %s.tar.gz ." % (env.project_tar_source + env.project_pack_name))
    print green("creating source package success!")


# 上传任务
@task
def put_package():
    print yellow("start put package...")
    with settings(warn_only=True):
        with cd(env.deploy_project_root + env.deploy_release_dir):  # cd /var/www/html/releases/
            run("mkdir %s" % (env.deploy_version))  # 创建版本目录
    env.deploy_full_path = env.deploy_project_root + env.deploy_release_dir + "/" + env.deploy_version
    with settings(warn_only=True):  # 上传项目压缩包到此目录
        result = put(env.project_tar_source + env.project_pack_name + ".tar.gz", env.deploy_full_path)
    if result.failed and not ("put file failed,Continue[Y/N]:?"):
        abort("aborting file put task!")
    with cd(env.deploy_full_path):  # 解压后删除压缩包
        run("tar -zxcf %s.tar.gz" % (env.project_pack_name))
        run("rm -rf %s.tar.gz" % (env.project_pack_name))
    print green("put & untar package success!")


# 当前版本目录软连接
@task
def make_symlink():
    print(yellow("update current symlink"))
    env.deploy_full_path = env.deploy_project_root + env.deploy_release_dir + "/" + env.deploy_version
    # 删除软连接,重新创建并指定软链源目录,新版本生效
    with settings(warn_only=True):
        run("rm -rf %s" % (env.deploy_project_root + env.deploy_current_dir))
        run("ln -s %s %s" % (env.deploy_full_path, env.deploy_project_root + env.deploy_current_dir))
    print green("make symlink success!")


# 版本回滚任务
@task
def rollback():
    print yellow("rollback project version")
    versionid = input_versionid()  # 获得用户输入回滚版本号
    if versionid == '':
        abort("project version ID error,abort!")
    env.deploy_full_path = env.deploy_project_root + env.deploy_release_dir + "/" + versionid
    run("rm -rf %s" % (env.deploy_project_root + env.deploy_current_dir))
    run("ln -s %s %s" % (env.deploy_full_path, env.deploy_project_root + env.deploy_current_dir))
    # 删除软链接，重新创建并指定软链源目的，新版本生效
    print(green("rollback success!"))


@task
def go():
    tar_source()
    put_package()
    make_symlink()