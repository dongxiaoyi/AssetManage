#_*_encoding:utf-8_*_
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import  ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from users.utils.mixin_utils import LoginRequiredMixin
from hostlist.models import AccHostList,MinionGroups
from .forms import MinionCmdForm
from scripts.script.saltcmd import saltcommands
from fileupload.models import UploadFiles
from .models import Service
from .forms import DevServiceForm,UpdateDevServiceForm,PullDevServicesTestForm,PullservicesnamesForm,PullDevServicesTestSelectForm,PullDevServicesForm,PullDevServicesSelectForm
from AssetManage.settings import MEDIA_ROOT
import json,os,types,subprocess,tarfile,zipfile,shutil
# Create your views here.

'''开发环境服务创建'''
class SaltDeployDevView(LoginRequiredMixin,View):
    def get(self,request):
        all_sevices = Service.objects.all()
        all_service_dev = Service.objects.filter(envtag='dev')
        all_files = UploadFiles.objects.all()
        return render(request,'salt_deploy_dev.html',{
            'all_service_dev': all_service_dev,
            'all_files': all_files,
        })
    def post(self,request):
        serviceform = DevServiceForm(request.POST)
        all_sevices = Service.objects.all()
        all_service_dev = Service.objects.filter(envtag='dev')
        all_files = UploadFiles.objects.all()
        DEV_BASEDIR = '/etc/salt/dev/services/'
        if os.path.exists(DEV_BASEDIR) == False:
            os.makedirs(DEV_BASEDIR)
        if serviceform.is_valid():
            servicename = request.POST.get('servicename','')
            sls = request.POST.get('sls','')
            all_service_name = []
            FILENAME = str(servicename) + '.sls'
            if all_sevices == []:
                with open(os.path.join(DEV_BASEDIR,FILENAME),'w+') as slsfile:
                    slsfile.write(sls)
                service_add = Service.objects.create(name=str(servicename),
                                                     envtag='dev',
                                                     sls=sls)
                service_add.save()
                msg = u'创建成功！'
                return render(request,'salt_deploy_dev.html',{
                'msg':msg,
                'all_service_dev': all_service_dev,
                'all_files': all_files,
                })
            else:
                FILENAME = str(servicename) + '.sls'
                for service in all_sevices:
                    all_service_name.append(str(service.name))
                if str(servicename) in all_service_name:
                    msg = u'服务已存在，禁止重复创建！'
                    return render(request, 'salt_deploy_dev.html', {
                        'msg': msg,
                        'all_service_dev': all_service_dev,
                        'all_files': all_files,
                    })
                else:
                    with open(os.path.join(DEV_BASEDIR, FILENAME),'w') as slsfile:
                        slsfile.write(sls)
                    service_add = Service.objects.create(name=str(servicename),
                                                         envtag='dev',
                                                         sls=sls)
                    service_add.save()
                    msg = u'创建成功！'
                    return render(request, 'salt_deploy_dev.html', {
                        'msg': msg,
                        'all_service_dev': all_service_dev,
                        'all_files': all_files,
                    })
        else:
            msg = u'创建失败，请检查输入是否有误！'
            return render(request, 'salt_deploy_dev.html', {
                'msg':msg,
                'all_service_dev': all_service_dev,
                'all_files': all_files,
            })





'''命令交互'''
class SaltExecuteView(LoginRequiredMixin,View):
    def get(self,request):
        all_acc_minion = AccHostList.objects.all()
        all_groups = MinionGroups.objects.all()
        return render(request,'salt_excute.html',{
            'all_acc_minion': all_acc_minion,
            'all_groups': all_groups,
        })
    def post(self,request):
        all_acc_minion = AccHostList.objects.all()
        minioncmd_form = MinionCmdForm(request.POST)
        all_groups = MinionGroups.objects.all()

        if minioncmd_form.is_valid():
            minionid_get = request.POST.getlist("minions", "")
            minionid = []
            for miid in minionid_get:
                minionid.append(str(miid))
            cmd = request.POST.get("cmd", "")
            groups = request.POST.getlist("groups",'')
            if minionid == []:
                if groups == '':
                    result = ''
                else:
                    all_minionid = []
                    for group in groups:
                        Group_que = MinionGroups.objects.get(Group=str(group))
                        group_que_id = Group_que.id
                        Group = MinionGroups.objects.get(id=group_que_id)
                        if Group.minion.all() == []:
                            pass
                        else:
                            for minion in Group.minion.all():
                                for minion_save in  (minion.minionid).split('\n'):
                                    #print minion_save
                                    all_minionid.append(str(minion_save))
                                    #print all_minionid
                                    all_minionid = list(set(all_minionid) | set(minionid))
                                    #print all_minionid
                        result = saltcommands(all_minionid,cmd)
            elif minionid !=[]:
                if groups == '':
                    all_minionid = minionid
                    result = saltcommands(all_minionid, cmd)
                else:
                    all_minionid = []
                    for group in groups:
                        Group_que = MinionGroups.objects.get(Group=str(group))
                        group_que_id = Group_que.id
                        groupminion = []
                        Group = MinionGroups.objects.get(id=group_que_id)
                        for minion_group  in Group.minion.all():
                            groupminion.append(minion_group)
                        if groupminion == []:
                            all_minionid = list(set(all_minionid) | set(minionid))
                        else:
                            for minion in Group.minion.all():
                                #print minion
                                for minion_save in  (minion.minionid).split('\n'):
                                    #print minion_save
                                    all_minionid.append(str(minion_save))
                                    #print all_minionid
                                    all_minionid = list(set(all_minionid) | set(minionid))
                        #print all_minionid
                    result = saltcommands(all_minionid,cmd)
                    #print result
            return render(request, 'salt_excute.html', {
                'all_acc_minion': all_acc_minion,
                'all_groups': all_groups,
                'result':result,
            })
        else:
            return render(request, 'salt_excute.html', {
                'all_acc_minion': all_acc_minion,
                'all_groups': all_groups,
            })


'''测试与推送开发环境服务'''
class PullDevServicesTestView(LoginRequiredMixin,View):
    def post(self,request):
        pulldevservicetestselectnamesforms = PullDevServicesTestSelectForm(request.POST)
        pullservicetestforms = PullDevServicesTestForm(request.POST)
        print pullservicetestforms
        pulldevserviceselectform = PullDevServicesForm(request.POST)
        pulldevservicesselectform = PullDevServicesSelectForm(request.POST)
        if pulldevservicetestselectnamesforms.is_valid():
            print '批量成功'
            pulldevservicestestselectnames = request.POST.getlist('pulldevservicestestselectnames','')
            service_minions = {}
            for pullservicename in pulldevservicestestselectnames:
                pullservice_query = Service.objects.get(name=str(pullservicename))
                pullserviceid = pullservice_query.id
                pulltestminions = pullservice_query.minions.all()
                pulltestgroups = pullservice_query.groups.all()
                minionsnames = []
                if pulltestminions == []:
                    for group in pulltestgroups:
                        minions_query = group.minion.all()
                        if minions_query == []:
                            pass
                        else:
                            for minion_query in minions_query:
                                minionid = minion_query.minionid
                                minionsnames.append(str(minionid))
                                minionsnames = list(set(minionsnames))
                        service_minions[str(pullservicename)] = minionsnames
                else:
                    if pulltestgroups == []:
                        for minion in pulltestminions:
                            minionname = minion.minionid
                            minionsnames.append(minionname)
                        service_minions[str(pullservicename)] = minionsnames
                    else:
                        for minion in pulltestminions:
                            minionname = minion.minionid
                            minionsnames.append(minionname)
                        for group in pulltestgroups:
                            minions_query = group.minion.all()
                            if minions_query == []:
                                pass
                            else:
                                for minion_query in minions_query:
                                    minionid = minion_query.minionid
                                    minionsnames.append(str(minionid))
                                    minionsnames = list(set(minionsnames))
                        service_minions[str(pullservicename)] = minionsnames
            SAVE_DIR = os.path.join(MEDIA_ROOT, 'upload/sls')
            msg = {}
            top_path = '/etc/salt/top.sls'
            for servicename,minions in service_minions.items():
                file_path = '/etc/salt/dev/services/' + str(servicename)
                service_que = Service.objects.get(name=str(servicename))
                servicefile = service_que.file
                fileid = servicefile.id
                pullfile = UploadFiles.objects.get(id=fileid)
                filename = pullfile.name
                if os.path.exists(file_path):
                    shutil.rmtree(file_path)
                    os.makedirs(file_path)
                else:
                    os.makedirs(file_path)
                file_path_extra = os.path.join(file_path, str(pullfile).split('.')[0])
                if os.path.exists(file_path_extra) == True:
                    shutil.rmtree(file_path_extra)
                    os.rmdir(file_path_extra)
                    if os.path.join(SAVE_DIR, str(pullfile)).split('.')[-1] == "gz":
                        tar_extra_command = 'tar xf ' + str(
                            os.path.join(SAVE_DIR, str(pullfile))) + ' -C ' + file_path
                        tar_extra = subprocess.Popen(tar_extra_command, stdout=subprocess.PIPE, shell=True)
                        tar_extra_stdout = tar_extra.communicate()[0]
                    elif os.path.join(SAVE_DIR, str(pullfile)).split('.')[-1] == "zip":
                        zip_extra_command = 'unzip ' + str(
                            os.path.join(SAVE_DIR, str(pullfile))) + ' -d ' + file_path
                        zip_extra = subprocess.Popen(zip_extra_command, stdout=subprocess.PIPE, shell=True)
                        zip_extra_stdout = zip_extra.communicate()[0]
                else:
                    if os.path.join(SAVE_DIR, str(pullfile)).split('.')[-1] == "gz":
                        tar_extra_command = 'tar xf ' + str(
                            os.path.join(SAVE_DIR, str(pullfile))) + ' -C ' + file_path
                        tar_extra = subprocess.Popen(tar_extra_command, stdout=subprocess.PIPE, shell=True)
                        tar_extra_stdout = tar_extra.communicate()[0]
                    elif os.path.join(SAVE_DIR, str(pullfile)).split('.')[-1] == "zip":
                        zip_extra_command = 'unzip ' + str(
                            os.path.join(SAVE_DIR, str(pullfile))) + ' -d ' + file_path
                        zip_extra = subprocess.Popen(zip_extra_command, stdout=subprocess.PIPE, shell=True)
                        zip_extra_stdout = zip_extra.communicate()[0]
                '''获取解压后目录名称'''
                dirs = {}
                for dir in os.listdir(file_path):
                    dirs[0] = str(dir)
                extra_dir = dirs[0]
                '''服务推送'''
                with open(top_path, 'wa') as top:
                    top.truncate()
                    top.write('dev:\n')
                    top.write("  \'*\':\n")
                    top.write("    - " + str(servicename) + "\n")
                for minion in minions:
                    pull_test_command = 'salt ' + str(minion) + ' state.highstate test=true'
                    pulltest = subprocess.Popen(pull_test_command, stdout=subprocess.PIPE, shell=True)
                    pulltest_stdout = pulltest.communicate()[0].decode('unicode_escape')
                    result = []
                    for cmd_line in pulltest_stdout.split('\n'):
                        cmd_line = cmd_line.replace(cmd_line, '<code>' + cmd_line + '</code>')
                        result.append(cmd_line)
                    msg['<ul class="nav nav-pills nav-stacked"><li class="active"><a href="#">' + u'主机： ' + minion + u'  服务： ' + servicename + '</a></li></ul>'] = result

            return render(request,'salt_deploy_dev_pull_test_result.html',{'msg':msg,
                                                                               })
        elif pullservicetestforms.is_valid():
            pulldevservicestestnames = request.POST.get('pulldevservicestestnames', '')
            print pulldevservicestestnames
            pulldevservicetest = Service.objects.get(name=str(pulldevservicestestnames))
            pulldevservicetestcode = pulldevservicetest.id
            pulldevtestminions = request.POST.getlist('pulldevtestminions', '')
            print pulldevtestminions
            pulldevtestfile = request.POST.get('pulldevtestfile', '')
            join_service = Service.objects.get(id=str(pulldevservicetestcode))
            pullsls = pulldevservicetest.sls
            all_acc_minion = AccHostList.objects.all()
            all_groups = MinionGroups.objects.all()
            all_sevices = Service.objects.all()
            all_service_dev = Service.objects.filter(envtag='dev')
            all_files = UploadFiles.objects.all()
            SAVE_DIR = os.path.join(MEDIA_ROOT, 'upload/sls')
            msg = {}
            top_path = '/etc/salt/top.sls'
            '''解压配置文件包，并做判断'''
            file_path = '/etc/salt/dev/services/' + str(pulldevservicestestnames)
            if os.path.exists(file_path):
                shutil.rmtree(file_path)
                os.makedirs(file_path)
            else:
                os.makedirs(file_path)
            file_path_extra = os.path.join(file_path,str(pulldevtestfile).split('.')[0])
            if os.path.exists(file_path_extra) == True:
                shutil.rmtree(file_path_extra)
                os.rmdir(file_path_extra)
                if os.path.join(SAVE_DIR,str(pulldevtestfile)).split('.')[-1] == "gz":
                    tar_extra_command = 'tar xf ' + str(os.path.join(SAVE_DIR,str(pulldevtestfile))) + ' -C ' + file_path
                    tar_extra = subprocess.Popen(tar_extra_command, stdout=subprocess.PIPE, shell=True)
                    tar_extra_stdout = tar_extra.communicate()[0]
                elif os.path.join(SAVE_DIR,str(pulldevtestfile)).split('.')[-1] == "zip":
                    zip_extra_command = 'unzip ' + str(os.path.join(SAVE_DIR,str(pulldevtestfile))) + ' -d ' + file_path
                    zip_extra = subprocess.Popen(zip_extra_command, stdout=subprocess.PIPE, shell=True)
                    zip_extra_stdout = zip_extra.communicate()[0]
            else:
                if os.path.join(SAVE_DIR,str(pulldevtestfile)).split('.')[-1] == "gz":
                    tar_extra_command = 'tar xf ' + str(os.path.join(SAVE_DIR,str(pulldevtestfile))) + ' -C ' + file_path
                    tar_extra = subprocess.Popen(tar_extra_command, stdout=subprocess.PIPE, shell=True)
                    tar_extra_stdout = tar_extra.communicate()[0]
                elif os.path.join(SAVE_DIR,str(pulldevtestfile)).split('.')[-1] == "zip":
                    zip_extra_command = 'unzip ' + str(os.path.join(SAVE_DIR,str(pulldevtestfile))) + ' -d ' + file_path
                    zip_extra = subprocess.Popen(zip_extra_command, stdout=subprocess.PIPE, shell=True)
                    zip_extra_stdout = zip_extra.communicate()[0]
            '''获取解压后目录名称'''
            dirs = {}
            for dir in os.listdir(file_path):
                dirs[0] = str(dir)
            extra_dir = dirs[0]
            '''服务推送'''
            with open(top_path, 'wa') as top:
                top.truncate()
                top.write('dev:\n')
                top.write("  \'*\':\n")
                top.write("    - " + str(pulldevservicestestnames) + "\n")
            for minion in pulldevtestminions:
                pull_test_command = 'salt ' + str(minion) + ' state.highstate test=true'
                print '开始'
                pulltest = subprocess.Popen(pull_test_command, stdout=subprocess.PIPE, shell=True)
                pulltest_stdout = pulltest.communicate()[0].decode('unicode_escape')
                result = []
                for cmd_line in pulltest_stdout.split('\n'):
                    cmd_line = cmd_line.replace(cmd_line, '<code>' + cmd_line + '</code>')
                    result.append(cmd_line)
                msg['<ul class="nav nav-pills nav-stacked"><li class="active"><a href="#">' + u'主机： ' + minion + u'  服务： ' + pulldevservicestestnames + '</a></li></ul>'] = result
            return render(request,'salt_deploy_dev_pull_test_result.html',{'msg':msg,
                                                                           'pulldevservicestestnames':pulldevservicestestnames,
                                                                           })

        elif pulldevserviceselectform.is_valid():
            pulldevservicestestnames = request.POST.get('pulldevservicestestnames', '')
            pulldevservicetest = Service.objects.get(name=str(pulldevservicestestnames))
            pulldevservicetestcode = pulldevservicetest.id
            pulldevtestminions = request.POST.getlist('pulldevtestminions', '')
            print pulldevtestminions
            pulldevtestfile = request.POST.get('pulldevtestfile', '')
            join_service = Service.objects.get(id=str(pulldevservicetestcode))
            pullsls = pulldevservicetest.sls
            all_acc_minion = AccHostList.objects.all()
            all_groups = MinionGroups.objects.all()
            all_sevices = Service.objects.all()
            all_service_dev = Service.objects.filter(envtag='dev')
            all_files = UploadFiles.objects.all()
            SAVE_DIR = os.path.join(MEDIA_ROOT, 'upload/sls')
            msg = {}
            top_path = '/etc/salt/top.sls'
            '''解压配置文件包，并做判断'''
            file_path = '/etc/salt/dev/services/' + str(pulldevservicestestnames)
            if os.path.exists(file_path):
                shutil.rmtree(file_path)
                os.makedirs(file_path)
            else:
                os.makedirs(file_path)
            file_path_extra = os.path.join(file_path, str(pulldevtestfile).split('.')[0])
            if os.path.exists(file_path_extra) == True:
                shutil.rmtree(file_path_extra)
                os.rmdir(file_path_extra)
                if os.path.join(SAVE_DIR, str(pulldevtestfile)).split('.')[-1] == "gz":
                    tar_extra_command = 'tar xf ' + str(
                        os.path.join(SAVE_DIR, str(pulldevtestfile))) + ' -C ' + file_path
                    tar_extra = subprocess.Popen(tar_extra_command, stdout=subprocess.PIPE, shell=True)
                    tar_extra_stdout = tar_extra.communicate()[0]
                elif os.path.join(SAVE_DIR, str(pulldevtestfile)).split('.')[-1] == "zip":
                    zip_extra_command = 'unzip ' + str(
                        os.path.join(SAVE_DIR, str(pulldevtestfile))) + ' -d ' + file_path
                    zip_extra = subprocess.Popen(zip_extra_command, stdout=subprocess.PIPE, shell=True)
                    zip_extra_stdout = zip_extra.communicate()[0]
            else:
                if os.path.join(SAVE_DIR, str(pulldevtestfile)).split('.')[-1] == "gz":
                    tar_extra_command = 'tar xf ' + str(
                        os.path.join(SAVE_DIR, str(pulldevtestfile))) + ' -C ' + file_path
                    tar_extra = subprocess.Popen(tar_extra_command, stdout=subprocess.PIPE, shell=True)
                    tar_extra_stdout = tar_extra.communicate()[0]
                elif os.path.join(SAVE_DIR, str(pulldevtestfile)).split('.')[-1] == "zip":
                    zip_extra_command = 'unzip ' + str(
                        os.path.join(SAVE_DIR, str(pulldevtestfile))) + ' -d ' + file_path
                    zip_extra = subprocess.Popen(zip_extra_command, stdout=subprocess.PIPE, shell=True)
                    zip_extra_stdout = zip_extra.communicate()[0]
            '''获取解压后目录名称'''
            dirs = {}
            for dir in os.listdir(file_path):
                dirs[0] = str(dir)
            extra_dir = dirs[0]
            '''服务推送'''
            with open(top_path, 'wa') as top:
                top.truncate()
                top.write('dev:\n')
                top.write("  \'*\':\n")
                top.write("    - " + str(pulldevservicestestnames) + "\n")
            for minion in pulldevtestminions:
                pull_test_command = 'salt ' + str(minion) + ' state.highstate'
                print '开始'
                pulltest = subprocess.Popen(pull_test_command, stdout=subprocess.PIPE, shell=True)
                pulltest_stdout = pulltest.communicate()[0].decode('unicode_escape')
                result = []
                for cmd_line in pulltest_stdout.split('\n'):
                    cmd_line = cmd_line.replace(cmd_line, '<code>' + cmd_line + '</code>')
                    result.append(cmd_line)
                msg['<ul class="nav nav-pills nav-stacked"><li class="active"><a href="#">' + u'主机： ' + minion + u'  服务： ' + pulldevservicestestnames + '</a></li></ul>'] = result
            return render(request, 'salt_deploy_dev_pull_test_result.html', {'msg': msg,
                                                                             'pulldevservicestestnames': pulldevservicestestnames,
                                                                             })
        elif pulldevservicesselectform.is_valid():
            pulldevservicestestselectnames = request.POST.getlist('pulldevservicestestselectnames', '')
            service_minions = {}
            for pullservicename in pulldevservicestestselectnames:
                pullservice_query = Service.objects.get(name=str(pullservicename))
                pullserviceid = pullservice_query.id
                pulltestminions = pullservice_query.minions.all()
                pulltestgroups = pullservice_query.groups.all()
                minionsnames = []
                if pulltestminions == []:
                    for group in pulltestgroups:
                        minions_query = group.minion.all()
                        if minions_query == []:
                            pass
                        else:
                            for minion_query in minions_query:
                                minionid = minion_query.minionid
                                minionsnames.append(str(minionid))
                                minionsnames = list(set(minionsnames))
                        service_minions[str(pullservicename)] = minionsnames
                else:
                    if pulltestgroups == []:
                        for minion in pulltestminions:
                            minionname = minion.minionid
                            minionsnames.append(minionname)
                        service_minions[str(pullservicename)] = minionsnames
                    else:
                        for minion in pulltestminions:
                            minionname = minion.minionid
                            minionsnames.append(minionname)
                        for group in pulltestgroups:
                            minions_query = group.minion.all()
                            if minions_query == []:
                                pass
                            else:
                                for minion_query in minions_query:
                                    minionid = minion_query.minionid
                                    minionsnames.append(str(minionid))
                                    minionsnames = list(set(minionsnames))
                        service_minions[str(pullservicename)] = minionsnames
            SAVE_DIR = os.path.join(MEDIA_ROOT, 'upload/sls')
            msg = {}
            top_path = '/etc/salt/top.sls'
            for servicename, minions in service_minions.items():
                file_path = '/etc/salt/dev/services/' + str(servicename)
                service_que = Service.objects.get(name=str(servicename))
                servicefile = service_que.file
                fileid = servicefile.id
                pullfile = UploadFiles.objects.get(id=fileid)
                filename = pullfile.name
                if os.path.exists(file_path):
                    shutil.rmtree(file_path)
                    os.makedirs(file_path)
                else:
                    os.makedirs(file_path)
                file_path_extra = os.path.join(file_path, str(pullfile).split('.')[0])
                if os.path.exists(file_path_extra) == True:
                    shutil.rmtree(file_path_extra)
                    os.rmdir(file_path_extra)
                    if os.path.join(SAVE_DIR, str(pullfile)).split('.')[-1] == "gz":
                        tar_extra_command = 'tar xf ' + str(
                            os.path.join(SAVE_DIR, str(pullfile))) + ' -C ' + file_path
                        tar_extra = subprocess.Popen(tar_extra_command, stdout=subprocess.PIPE, shell=True)
                        tar_extra_stdout = tar_extra.communicate()[0]
                    elif os.path.join(SAVE_DIR, str(pullfile)).split('.')[-1] == "zip":
                        zip_extra_command = 'unzip ' + str(
                            os.path.join(SAVE_DIR, str(pullfile))) + ' -d ' + file_path
                        zip_extra = subprocess.Popen(zip_extra_command, stdout=subprocess.PIPE, shell=True)
                        zip_extra_stdout = zip_extra.communicate()[0]
                else:
                    if os.path.join(SAVE_DIR, str(pullfile)).split('.')[-1] == "gz":
                        tar_extra_command = 'tar xf ' + str(
                            os.path.join(SAVE_DIR, str(pullfile))) + ' -C ' + file_path
                        tar_extra = subprocess.Popen(tar_extra_command, stdout=subprocess.PIPE, shell=True)
                        tar_extra_stdout = tar_extra.communicate()[0]
                    elif os.path.join(SAVE_DIR, str(pullfile)).split('.')[-1] == "zip":
                        zip_extra_command = 'unzip ' + str(
                            os.path.join(SAVE_DIR, str(pullfile))) + ' -d ' + file_path
                        zip_extra = subprocess.Popen(zip_extra_command, stdout=subprocess.PIPE, shell=True)
                        zip_extra_stdout = zip_extra.communicate()[0]
                '''获取解压后目录名称'''
                dirs = {}
                for dir in os.listdir(file_path):
                    dirs[0] = str(dir)
                extra_dir = dirs[0]
                '''服务推送'''
                with open(top_path, 'wa') as top:
                    top.truncate()
                    top.write('dev:\n')
                    top.write("  \'*\':\n")
                    top.write("    - " + str(servicename) + "\n")
                for minion in minions:
                    pull_test_command = 'salt ' + str(minion) + ' state.highstate'
                    pulltest = subprocess.Popen(pull_test_command, stdout=subprocess.PIPE, shell=True)
                    pulltest_stdout = pulltest.communicate()[0].decode('unicode_escape')
                    result = []
                    for cmd_line in pulltest_stdout.split('\n'):
                        cmd_line = cmd_line.replace(cmd_line, '<code>' + cmd_line + '</code>')
                        result.append(cmd_line)
                    msg['<ul class="nav nav-pills nav-stacked"><li class="active"><a href="#">' + u'主机： ' + minion + u'  服务： ' + servicename + '</a></li></ul>'] = result

            return render(request, 'salt_deploy_dev_pull_test_result.html', {'msg': msg,
                                                                             })
        else:
            msg = {}
            msg['<ul class="nav nav-pills nav-stacked"><li class="active"><a href="#">' + u'异常： '+ '</a></li></ul>'] = u'未知错误，请重新尝试操作！'
            return render(request, 'salt_deploy_dev_pull_test_result.html', {'msg': msg,
                                                                             })


            #pulltest_command = "salt " + str('') + " state.highstate"
            #pulltest = subprocess.Popen(pulltest_command, stdout=subprocess.PIPE, shell=True)
            #pulltest_stdout = pulltest.communicate()[0].split('\n')
            #with open(top_path, 'a') as top:
            #    top.truncate()
            #    top.write('dev:\n')
            #    top.write("\'  \*:'\n")
            #for minion in pulldevtestminions:
            #    top.write("    - " + str(pulldevservicestestnames))
#
            #    pulltest_command = "salt " + str(minion) + " state.highstate"
            #    pulltest = subprocess.Popen(pulltest_command,stdout=subprocess.PIPE,shell=True)
            #    pulltest_stdout = pulltest.communicate()[0].split('\n')
            #    msg[str(minion)] = pulltest_stdout
            #return

'''开发服务推送选择服务界面'''
class PullDevServicesView(LoginRequiredMixin, View):
    def post(self, request):
        pulldevservicesnames = PullservicesnamesForm(request.POST)
        all_service_dev = Service.objects.filter(envtag='dev')
        if pulldevservicesnames.is_valid():
            pulldevservicesnames = request.POST.getlist('pulldevservicesnames', '')
            remove_service = {}
            service_minions_dict = {}
            for servicename in pulldevservicesnames:
                get_service_query = Service.objects.get(name=str(servicename))
                get_service_minions = []
                for minion in get_service_query.minions.all():
                    get_service_minions.append(minion)
                get_service_groups = []
                for group in get_service_query.groups.all():
                    get_service_groups.append(group)
                if get_service_minions == []:
                    if get_service_groups == []:
                        remove_service[str(servicename)] = u'推送服务主机与组别均为空！'
                        msg = u'请确保推送服务主机与组别不都为空！'
                        return render(request, 'salt_deploy_dev_pull.html', {'msg': msg,
                                                                             'all_service_dev': all_service_dev,
                                                                             })
                    else:

                        get_service_groups_minions = []
                        for service_group in get_service_groups:
                            for get_service_groups_minion in service_group.minion.all():
                                get_service_groups_minions.append(str(get_service_groups_minion))
                                get_service_groups_minions = list(set(get_service_groups_minions))
                        if get_service_groups_minions == []:
                            msg = u'推送服务主机为空，组别不为空，但组内主机都为空'
                            return render(request, 'salt_deploy_dev_pull.html', {'msg': msg,
                                                                                'all_service_dev': all_service_dev,
                                                                                })
                        else:
                            '''字典（服务--主机）-----发送到测试推送界面'''
                            service = Service.objects.get(name=str(servicename))
                            service_minions_dict[service] = get_service_groups_minions
                            #for minion in get_service_groups_minions:
                            #    pull_command = "salt " + str(minion) + ' states.highstate'
                            #    pull_service = subprocess.Popen(pull_command,stdout=subprocess.PIPE,shell=True)
                            #    pull_stdout = pull_service.communicate()[0].split('\n')
                            #    service_minions_dict[str(minion)] = pull_stdout
                else:
                    '''服务的主机为空，判断组别是否为空'''
                    get_minion_query_minoionid = []
                    for minion_query in get_service_minions:
                        get_minion_query_minoionid.append(str(minion_query.minionid))
                        get_minion_query_minoionid = list(set(get_minion_query_minoionid))
                    if get_service_groups == []:
                        service = Service.objects.get(name=str(servicename))
                        service_minions_dict[service] = get_minion_query_minoionid
                    else:
                        get_service_groups_minions = []
                        for service_group in get_service_groups:
                            for get_service_groups_minion in service_group.minion.all():
                                get_service_groups_minions.append(get_service_groups_minion)
                                get_service_groups_minions = list(set(get_service_groups_minions))
                        print get_service_groups_minions
                        if get_service_groups_minions == []:
                            service = Service.objects.get(name=str(servicename))
                            service_minions_dict[service] = get_minion_query_minoionid
                        else:
                            for minion_in_groups in get_service_groups_minions:
                                get_minion_query_minoionid.append(str(minion_in_groups.minionid))
                                get_minion_query_minoionid = list(set(get_minion_query_minoionid))
                            service = Service.objects.get(name=str(servicename))
                            service_minions_dict[service] = get_minion_query_minoionid
            return render(request, 'salt_deploy_dev_pull_test.html',
                          {'service_minions_dict': service_minions_dict,
                           'all_service_dev': all_service_dev,
                           })
        else:
            msg = u'尚未选择服务！'
            return render(request, 'salt_deploy_dev_pull.html', {'msg': msg,
                                                                 'all_service_dev': all_service_dev,
                                                                 })
            #minions = []
            #for group in pulldevservicesnames:
            #    group_query = MinionGroups.objects.get(Group=str(group))
            #    minion_query = group_query.minion.all()
            #    for minion_que in minion_query:
            #        for minion in minion_que.minionid.split('\n'):
            #            print minion
            #            minions.append(str(minion))
            #            minions = list(set(minions))
            #if minions == []:
            #    msg = '推送服务内主机不可再全部为空！'
            #    return render(request, 'salt_deploy_dev_pull.html', {'msg': msg,
            #                                                         'all_service_dev': all_service_dev,
            #                                                         })
            #return render(request,'salt_deploy_dev_pull_test.html')

    def get(self,request):
        all_service_dev = Service.objects.filter(envtag='dev')
        return render(request,'salt_deploy_dev_pull.html', {'all_service_dev': all_service_dev,
                                                            })

'''开发服务配置更新'''
class UpdateDevServiceView(LoginRequiredMixin,View):
    def post(self,request):
        SAVE_DIR = os.path.join(MEDIA_ROOT, 'upload/sls')
        updatedevserviceform = UpdateDevServiceForm(request.POST)
        DEV_BASEDIR = '/etc/salt/dev/services/'
        if updatedevserviceform.is_valid():
            updatedevservicename = request.POST.get('updatedevservicename','')
            updatedevservice = Service.objects.get(name=str(updatedevservicename))
            updatedevservicecode = updatedevservice.id
            updatedevminions = request.POST.getlist('updatedevminions','')
            updatedevgroups = request.POST.getlist('updatedevgroups','')
            updatedevfilename = request.POST.get('updatedevfilename','')
            updatedevsls = request.POST.get('updatedevsls','')
            file_queryset = UploadFiles.objects.get(name=str(updatedevfilename))
            file_id = file_queryset.id
            file_path = os.path.join(SAVE_DIR,str(updatedevfilename))
            FILENAME = str(updatedevservicename) + '.sls'
            print type(updatedevminions)
            print type(updatedevgroups)
            if type(updatedevminions) == types.StringType:
                if type(updatedevgroups) == types.StringType:
                    updateservice = Service.objects.filter(name=str(updatedevservicename)).update(envtag='dev',
                                                                                                  sls=updatedevsls,
                                                                                                  file_id=file_id)
                    with open(os.path.join(DEV_BASEDIR, FILENAME), 'w') as slsfile:
                        slsfile.write(updatedevsls)
                    # 清空minion
                    updateminionservice = Service.objects.get(name=str(updatedevservicename))
                    all_minions = updateminionservice.minions.all()
                    updateminionservice.minions.clear()
                    #for minion in all_minions:
                    #    updateminionservice.minions.delate(minion)
                    # 清空groups
                    updategroupservice = Service.objects.get(name=str(updatedevservicename))
                    all_groups = updategroupservice.groups.all()
                    updategroupservice.groups.clear()
                    #for group in all_groups:
                    #    updategroupservice.groups.delete(id=group.id)
                    from django.core.urlresolvers import reverse
                    return HttpResponseRedirect(reverse('fileupload:upload_join',args=[str(updatedevservicecode),]))
                else:
                    updateservice = Service.objects.filter(name=str(updatedevservicename)).update(envtag='dev',
                                                                                                  sls=updatedevsls,
                                                                                                  file_id=file_id)
                    with open(os.path.join(DEV_BASEDIR, FILENAME), 'w') as slsfile:
                        slsfile.write(updatedevsls)
                    # 清空minion
                    updateminionservice = Service.objects.get(name=str(updatedevservicename))
                    all_minions = updateminionservice.minions.all()
                    updateminionservice.minions.clear()
                    #for minion in all_minions:
                    #    updateminionservice.minions.delete(id=minion.id)
                    # 更新groups
                    updategroupservice = Service.objects.get(name=str(updatedevservicename))
                    updategroupserviceid = updategroupservice.id
                    update_group_query = []
                    for group in updatedevgroups:
                        group_query = MinionGroups.objects.get(Group=str(group))
                        update_group_query.append(group_query)
                    updategroupservice.groups.clear()
                    for query_group in update_group_query:
                        updategroupservice.groups.add(query_group)
                    from django.core.urlresolvers import reverse
                    return HttpResponseRedirect(reverse('fileupload:upload_join',args=[str(updatedevservicecode),]))
            else:
                if type(updatedevgroups) == types.StringType:
                    updateservice = Service.objects.filter(name=str(updatedevservicename)).update(envtag='dev',
                                                                                                  sls=updatedevsls,
                                                                                                  file_id=file_id)
                    with open(os.path.join(DEV_BASEDIR, FILENAME), 'w') as slsfile:
                        slsfile.write(updatedevsls)
                    #更新minion
                    updateminionservice = Service.objects.get(name=str(updatedevservicename))
                    updateminionserviceid = updateminionservice.id
                    update_minion_query = []
                    for minionid in updatedevminions:
                        minion_query = AccHostList.objects.get(minionid=str(minionid))
                        update_minion_query.append(minion_query)
                    updateminionservice.minions.clear()
                    for query_minion in update_minion_query:
                        updateminionservice.minions.add(query_minion)
                    # 清空groups
                    updategroupservice = Service.objects.get(name=str(updatedevservicename))
                    all_groups = updategroupservice.groups.all()
                    updategroupservice.groups.clear()
                    #for group in all_groups:
                    #    updategroupservice.groups.delete(id=group.id)
                    from django.core.urlresolvers import reverse
                    return HttpResponseRedirect(reverse('fileupload:upload_join',args=[str(updatedevservicecode),]))
                else:
                    updateservice = Service.objects.filter(name=str(updatedevservicename)).update(envtag='dev',
                                                                                                  sls=updatedevsls,
                                                                                                  file_id=file_id)
                    with open(os.path.join(DEV_BASEDIR, FILENAME), 'w') as slsfile:
                        slsfile.write(updatedevsls)
                    # 更新minion
                    updateminionservice = Service.objects.get(name=str(updatedevservicename))
                    updateminionserviceid = updateminionservice.id
                    update_minion_query = []
                    for minionid in updatedevminions:
                        minion_query = AccHostList.objects.get(minionid=str(minionid))
                        update_minion_query.append(minion_query)
                    updateminionservice.minions.clear()
                    for query_minion in update_minion_query:
                        updateminionservice.minions.add(query_minion)
                    #更新groups
                    updategroupservice = Service.objects.get(name=str(updatedevservicename))
                    updategroupserviceid = updategroupservice.id
                    update_group_query = []
                    for group in updatedevgroups:
                        group_query = MinionGroups.objects.get(Group=str(group))
                        update_group_query.append(group_query)
                    updategroupservice.groups.clear()
                    for query_group in update_group_query:
                        updategroupservice.groups.add(query_group)
                    from django.core.urlresolvers import reverse
                    return HttpResponseRedirect(reverse('fileupload:upload_join',args=[str(updatedevservicecode),]))
        else:
            updatedevservicename = request.POST.get('updatedevservicename', '')
            updatedevservice = Service.objects.get(name=str(updatedevservicename))
            updatedevservicecode = updatedevservice.id
            from django.core.urlresolvers import reverse
            return HttpResponseRedirect(reverse('fileupload:upload_join', args=[str(updatedevservicecode), ]))
            #updatedevgroups_queryset = []
                    #for updatedevgroup in updatedevgroups:
                    #    updatedevgroup_queryset = MinionGroups.objects.get(Group=str(updatedevgroup))
                    #    updatedevgroup_queryset_id =  updatedevgroup_queryset.id
            #updatedevminions_queryset = []
            #for updatedevminionname in updatedevminions:
            #    updatedevminion_queryset = AccHostList(minionid=str(updatedevminionname))
            #    updatedevminions_queryset.append(updatedevminion_queryset)
