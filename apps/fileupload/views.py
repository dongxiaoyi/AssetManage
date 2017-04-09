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
from .models import UploadFiles
from .forms import UploadFilesForm
import json,os,sys
from AssetManage.settings import MEDIA_ROOT
from saltstack.models import Service
import subprocess,re
from hostlist.models import AccHostList,MinionGroups

# Create your views here.

# Create your views here.
class  UploadView(LoginRequiredMixin,View):

    def post(self,request):
        fileform = UploadFilesForm(request.POST,request.FILES)
        all_service_dev = Service.objects.filter(envtag='dev')
        all_files = UploadFiles.objects.all()
        if fileform.is_valid():
            print '开始上传'
            filesource = request.FILES.get('filesource','')
            SAVE_DIR = os.path.join(MEDIA_ROOT,'upload/sls')
            if os.path.exists(SAVE_DIR) == False:
                os.makedirs(SAVE_DIR)
                f = open(os.path.join(SAVE_DIR, filesource.name), 'wb')
                for line in filesource.chunks():
                    f.write(line)
                f.close()
                all_files = os.walk(SAVE_DIR)
                UploadFiles.objects.all().delete()
                for dirname,dirs,file in all_files:
                    for filename in file:
                        file_db = UploadFiles.objects.create(name=str(filename))
                        file_db.save()
                from django.core.urlresolvers import reverse
                return HttpResponseRedirect(reverse('salt:salt_deploy_dev'))
            elif os.path.exists(SAVE_DIR) == True:
                f = open(os.path.join(SAVE_DIR, filesource.name), 'wb')
                for line in filesource.chunks():
                    f.write(line)
                f.close()
                all_files = os.walk(SAVE_DIR)
                UploadFiles.objects.all().delete()
                for dirname,dirs,file in all_files:
                    for filename in file:
                        file_db = UploadFiles.objects.create(name=str(filename))
                        file_db.save()
                from django.core.urlresolvers import reverse
                return HttpResponseRedirect(reverse('salt:salt_deploy_dev'))
        else:
            from django.core.urlresolvers import reverse
            return HttpResponseRedirect(reverse('salt:salt_deploy_dev'))

class UploadGitView(LoginRequiredMixin,View):

    def post(self,request):
        git = request.POST.get('gitaddr','')
        list_dir = []
        if str(git) == '':
            from django.core.urlresolvers import reverse
            return HttpResponseRedirect(reverse('salt:salt_deploy_dev'))
        else:
            git_dir = re.split('\.|/',git)
            git_file_dir =  git_dir[-2]
            SAVE_DIR = os.path.join(MEDIA_ROOT, 'upload/sls')
            GIT_DIR = SAVE_DIR + '/' + git_file_dir
            if os.path.exists(GIT_DIR) == True:
                rm_fr_git_dir_cmd = 'rm -fr ' + SAVE_DIR + '/' + git_file_dir
                rm_fr_git_dir = subprocess.Popen(rm_fr_git_dir_cmd, stdout=subprocess.PIPE, shell=True)
                rm_fr_git_dir_stdout = rm_fr_git_dir.communicate()[0].strip()
                GIT_TAR = SAVE_DIR + '/' + git_file_dir + '.tar.gz'
                if os.path.exists(GIT_TAR) == True:
                    rm_fr_git_tar_cmd = 'rm -fr ' + GIT_TAR
                    rm_fr_git_tar = subprocess.Popen(rm_fr_git_tar_cmd, stdout=subprocess.PIPE, shell=True)
                    rm_fr_git_tar_stdout = rm_fr_git_tar.communicate()[0].strip()
                    re_get_git_file_cmd = 'git clone ' + str(git) + ' ' + SAVE_DIR
                    re_get_git_file = subprocess.Popen(re_get_git_file_cmd, stdout=subprocess.PIPE, shell=True)
                    re_get_git_file_stdout = re_get_git_file.communicate()[0].strip()
                    tar_git_dir_cmd = 'tar zcf ' + SAVE_DIR + '/' + git_file_dir + '.tar.gz ' + SAVE_DIR + '/' + git_file_dir
                    tar_git_dir = subprocess.Popen(tar_git_dir_cmd, stdout=subprocess.PIPE, shell=True)
                    tar_git_dir_stdout = tar_git_dir.communicate()[0].strip()
                    rm_fr_git_dir_cmd = 'rm -fr ' + SAVE_DIR + '/' + git_file_dir + '/'
                    rm_fr_git_dir = subprocess.Popen(rm_fr_git_dir_cmd, stdout=subprocess.PIPE, shell=True)
                    rm_fr_git_dir_stdout = rm_fr_git_dir.communicate()[0].strip()
                    git_file_db = UploadFiles.objects.get_or_create(name=str(git_file_dir))
                    from django.core.urlresolvers import reverse
                    return HttpResponseRedirect(reverse('salt:salt_deploy_dev'))
                else:
                    re_get_git_file_cmd = 'git clone ' + str(git) + ' ' + SAVE_DIR
                    re_get_git_file = subprocess.Popen(re_get_git_file_cmd, stdout=subprocess.PIPE, shell=True)
                    re_get_git_file_stdout = re_get_git_file.communicate()[0].strip()
                    tar_git_dir_cmd = 'tar zcf ' + SAVE_DIR + '/' + git_file_dir + '.tar.gz ' + SAVE_DIR + '/' + git_file_dir
                    tar_git_dir = subprocess.Popen(tar_git_dir_cmd, stdout=subprocess.PIPE, shell=True)
                    tar_git_dir_stdout = tar_git_dir.communicate()[0].strip()
                    rm_fr_git_dir_cmd = 'rm -fr ' + SAVE_DIR + '/' + git_file_dir + '/'
                    rm_fr_git_dir = subprocess.Popen(rm_fr_git_dir_cmd, stdout=subprocess.PIPE, shell=True)
                    rm_fr_git_dir_stdout = rm_fr_git_dir.communicate()[0].strip()
                    git_file_db = UploadFiles.objects.get_or_create(name=str(git_file_dir))
                    from django.core.urlresolvers import reverse
                    return HttpResponseRedirect(reverse('salt:salt_deploy_dev'))
            else:
                GIT_TAR = SAVE_DIR + '/' + git_file_dir + '.tar.gz'
                if os.path.exists(GIT_TAR) == True:
                    rm_fr_git_tar_cmd = 'rm -fr ' + GIT_TAR
                    rm_fr_git_tar = subprocess.Popen(rm_fr_git_tar_cmd, stdout=subprocess.PIPE, shell=True)
                    rm_fr_git_tar_stdout = rm_fr_git_tar.communicate()[0].strip()
                    re_get_git_file_cmd = 'git clone ' + str(git) + ' ' + SAVE_DIR
                    re_get_git_file = subprocess.Popen(re_get_git_file_cmd, stdout=subprocess.PIPE, shell=True)
                    re_get_git_file_stdout = re_get_git_file.communicate()[0].strip()
                    tar_git_dir_cmd = 'tar zcf ' + SAVE_DIR + '/' + git_file_dir + '.tar.gz ' + SAVE_DIR + '/' + git_file_dir
                    tar_git_dir = subprocess.Popen(tar_git_dir_cmd, stdout=subprocess.PIPE, shell=True)
                    tar_git_dir_stdout = tar_git_dir.communicate()[0].strip()
                    rm_fr_git_dir_cmd = 'rm -fr ' + SAVE_DIR + '/' + git_file_dir + '/'
                    rm_fr_git_dir = subprocess.Popen(rm_fr_git_dir_cmd, stdout=subprocess.PIPE, shell=True)
                    rm_fr_git_dir_stdout = rm_fr_git_dir.communicate()[0].strip()
                    git_file_db = UploadFiles.objects.get_or_create(name=str(git_file_dir))
                    from django.core.urlresolvers import reverse
                    return HttpResponseRedirect(reverse('salt:salt_deploy_dev'))
                else:
                    get_git_file_cmd = 'git clone ' + str(git) + ' ' + SAVE_DIR
                    get_git_file = subprocess.Popen(get_git_file_cmd,stdout=subprocess.PIPE,shell=True)
                    get_git_file_stdout = get_git_file.communicate()[0].strip()
                    tar_git_dir_cmd = 'tar zcf ' + SAVE_DIR + '/' + git_file_dir + '.tar.gz ' + SAVE_DIR + '/' + git_file_dir
                    tar_git_dir = subprocess.Popen(tar_git_dir_cmd,stdout=subprocess.PIPE,shell=True)
                    tar_git_dir_stdout = tar_git_dir.communicate()[0].strip()
                    rm_fr_git_dir_cmd = 'rm -fr ' + SAVE_DIR + '/' + git_file_dir + '/'
                    rm_fr_git_dir = subprocess.Popen(rm_fr_git_dir_cmd,stdout=subprocess.PIPE,shell=True)
                    rm_fr_git_dir_stdout = rm_fr_git_dir.communicate()[0].strip()
                    git_file_db = UploadFiles.objects.get_or_create(name=str(git_file_dir))
                    from django.core.urlresolvers import reverse
                    return HttpResponseRedirect(reverse('salt:salt_deploy_dev'))


class UploadJoinView(LoginRequiredMixin,View):

    def post(self,request):
        all_acc_minion = AccHostList.objects.all()
        all_groups = MinionGroups.objects.all()
        all_sevices = Service.objects.all()
        all_service_dev = Service.objects.filter(envtag='dev')
        all_files = UploadFiles.objects.all()
        return render(request,'salt_deploy_dev_join.html',{
            'all_acc_minion': all_acc_minion,
            'all_groups': all_groups,
            'all_service_dev': all_service_dev,
            'all_files': all_files,
            })

    def get(self,request,id_code):
        service_id = id_code
        print id_code
        join_service = Service.objects.get(id=str(id_code))
        all_acc_minion = AccHostList.objects.all()
        all_groups = MinionGroups.objects.all()
        all_sevices = Service.objects.all()
        all_service_dev = Service.objects.filter(envtag='dev')
        all_files = UploadFiles.objects.all()
        return render(request,'salt_deploy_dev_join.html',{
            'all_acc_minion': all_acc_minion,
            'all_groups': all_groups,
            'all_service_dev': all_service_dev,
            'all_files': all_files,
            'join_service':join_service,

            })

class UploadRemoveView(LoginRequiredMixin,View):
    def get(self,request):
        print u'开始删除'
        SAVE_DIR = os.path.join(MEDIA_ROOT, 'upload/sls')
        file_remove = request.GET.get('fileremove','')
        print file_remove
        file = os.path.join(SAVE_DIR,str(file_remove))
        remove_file_cmd = "rm -fr " + str(file)
        remove_file = subprocess.Popen(remove_file_cmd,stdout=subprocess.PIPE,shell=True)
        remove_file_out = remove_file.communicate()[0].strip()
        UploadFiles.objects.filter(name=str(file_remove)).delete()
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse('salt:salt_deploy_dev'))