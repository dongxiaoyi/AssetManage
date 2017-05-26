#_*_coding:utf-8_*_
from __future__ import unicode_literals

import os,sys,subprocess
os.path.join(os.path.dirname(__file__),'../../..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AssetManage.settings')
import django
django.setup()
# from django.core.exceptions import ObjectDoesNotExist
# from django.db.models import Q
from hostlist.models import AccHostList,UnAccHostList,ErrorHostList
#os.environ['DJANGO_SETTINGS_MODULE'] = 'AssetManage.settings'
#@app.task
'''获取minion端的信息'''


All_minion_cmd = subprocess.Popen("salt-key -l acc|grep -v Acc",stdout=subprocess.PIPE,shell=True)
All_minion = All_minion_cmd.communicate()[0].strip().split('\n')
minions = []
for minion in All_minion:
    minions.append(minion)

def get_all_osfinger():
    all_osfinger = {}
    for minion in minions:
        get_osfinger_cmd = "salt " + str(minion) + " grains.get osfinger|sed 'N;s/\\n//g'"
        get_osfinger = subprocess.Popen(get_osfinger_cmd,stdout=subprocess.PIPE,shell=True)
        os_finger = get_osfinger.communicate()[0].strip().split(':    ')
        all_osfinger[str(minion)] = str(os_finger[1])
    return all_osfinger

def get_all_mem_total():
    all_mem_total = {}
    for minion in minions:
        get_mem_total_cmd = "salt " + str(minion) + " grains.get mem_total|sed 'N;s/\\n//g'"
        get_mem_total = subprocess.Popen(get_mem_total_cmd,stdout=subprocess.PIPE,shell=True)
        mem_total = get_mem_total.communicate()[0].strip().split(':    ')
        all_mem_total[str(minion)] = str(mem_total[1])
    return all_mem_total

def get_all_cpu_model():
    all_cpu_model = {}
    for minion in minions:
        get_cpu_model_cmd = "salt " + str(minion) + " grains.get cpu_model|sed 'N;s/\\n//g'"
        get_cpu_model = subprocess.Popen(get_cpu_model_cmd,stdout=subprocess.PIPE,shell=True)
        cpu_model = get_cpu_model.communicate()[0].strip().split(':    ')
        all_cpu_model[str(minion)] = str(cpu_model[1])
    return all_cpu_model

def get_all_num_cpus():
    all_num_cpus = {}
    for minion in minions:
        get_num_cpus_cmd = "salt " + str(minion) + " grains.get num_cpus|sed 'N;s/\\n//g'"
        get_num_cpus = subprocess.Popen(get_num_cpus_cmd,stdout=subprocess.PIPE,shell=True)
        num_cpus = get_num_cpus.communicate()[0].strip().split(':    ')
        all_num_cpus[str(minion)] = str(num_cpus[1])
    return all_num_cpus

def get_all_cpuarch():
    all_cpuarch = {}
    for minion in minions:
        get_cpuarch_cmd = "salt " + str(minion) + " grains.get cpuarch|sed 'N;s/\\n//g'"
        get_cpuarch = subprocess.Popen(get_cpuarch_cmd,stdout=subprocess.PIPE,shell=True)
        cpuarch = get_cpuarch.communicate()[0].strip().split(':    ')
        all_cpuarch[str(minion)] = str(cpuarch[1])
    return all_cpuarch

def get_all_kernelrelease():
    all_kernelrelease = {}
    for minion in minions:
        get_kernelrelease_cmd = "salt " + str(minion) + " grains.get kernelrelease|sed 'N;s/\\n//g'"
        get_kernelrelease = subprocess.Popen(get_kernelrelease_cmd,stdout=subprocess.PIPE,shell=True)
        kernelrelease = get_kernelrelease.communicate()[0].strip().split(':    ')
        all_kernelrelease[str(minion)] = str(kernelrelease[1])
    return all_kernelrelease

def get_all_saltversion():
    all_saltversion = {}
    for minion in minions:
        get_saltversion_cmd = "salt " + str(minion) + " grains.get saltversion|grep -v '\- 172'|sed 'N;s/\\n//g'"
        get_saltversion = subprocess.Popen(get_saltversion_cmd,stdout=subprocess.PIPE,shell=True)
        saltversion = get_saltversion.communicate()[0].strip().split(':    ')
        all_saltversion[str(minion)] = str(saltversion[1])
    return all_saltversion

def get_all_fqdn_ip4():
    all_fqdn_ip4 = {}
    for minion in minions:
        get_fqdn_ip4_cmd = "salt " + str(minion) + " grains.get fqdn_ip4|head -2|sed 'N;s/\\n//g'|sed 's/:    - /:/g'"
        #get_fqdn_ip4_cmd = "salt " + str(minion) + " grains.get fqdn_ip4|head -2|sed 'N;s/\\n//g'|sed 's/:    /:/g'"
        get_fqdn_ip4 = subprocess.Popen(get_fqdn_ip4_cmd,stdout=subprocess.PIPE,shell=True)
        fqdn_ip4 = get_fqdn_ip4.communicate()[0].strip().split(':')
        all_fqdn_ip4[str(minion)] = str(fqdn_ip4[1])
    return all_fqdn_ip4

def get_all_host():
    all_host = {}
    for minion in minions:
        #get_host_cmd = "salt " + str(minion) + " grains.get host|head -2|sed 'N;s/\\n//g'|sed 's/:    - /:/g'"
        get_host_cmd = "salt " + str(minion) + " grains.get host|head -2|sed 'N;s/\\n//g'|sed 's/:    /:/g'"
        get_host = subprocess.Popen(get_host_cmd,stdout=subprocess.PIPE,shell=True)
        host = get_host.communicate()[0].strip().split(':')
        all_host[str(minion)] = str(host[1])
    return all_host

def GetMinionInfo():
    '''
    定时任务，推送通过验证的minion_id的资源信息到数据库
    :return:

    '''
    '''所有的资源信息'''
    all_osfinger = get_all_osfinger()
    all_fqdn_ip4 = get_all_fqdn_ip4()
    all_saltversion = get_all_saltversion()
    all_kernelrelease = get_all_kernelrelease()
    all_cpuarch = get_all_cpuarch()
    all_num_cpus = get_all_num_cpus()
    all_cpu_model = get_all_cpu_model()
    all_mem_total = get_all_mem_total()
    all_host = get_all_host()
    '''获取acc的minion_id'''
    get_acc_minion_id_cmd = "salt-key -l acc|grep -v Acc"
    get_acc_minion_id = subprocess.Popen(get_acc_minion_id_cmd,stdout=subprocess.PIPE,shell=True)
    acc_stdout = get_acc_minion_id.communicate()[0].strip().split('\n')
    '''获取unacc的minion_id'''
    get_unacc_minion_id_cmd = "salt-key -l una|grep -v Una"
    get_unacc_minion_id = subprocess.Popen(get_unacc_minion_id_cmd,stdout=subprocess.PIPE,shell=True)
    unacc_stdout = get_unacc_minion_id.communicate()[0].strip().split('\n')
    '''获取数据库中所有acc的minion的minionid'''
    all_acc_minionid = []
    all_acc_minion = AccHostList.objects.filter(key_tag='acc')
    if all_acc_minion == []:
        pass
    else:
        for minion in all_acc_minion:
            all_acc_minionid.append(str(minion.minionid))
    '''获取数据库中所有unacc的minion的minionid'''
    all_unacc_minionid = []
    all_unacc_minion = UnAccHostList.objects.filter(key_tag='unacc')
    if all_unacc_minion == []:
        pass
    else:
        for minion in all_unacc_minion:
            all_unacc_minionid.append(str(minion.minionid))
    #'''如果这个minionid本来就有，就更新数据，没有就创建数据,如果这个minionid在unacc中，自动创建acc，并且删除unacc数据'''
    #'''如果服务器返回的minionid为['']，得看一下数据库的是否为空！！！'''
    if acc_stdout == ['']:
        if all_acc_minion == []:
            pass
        else:
            '''如果数据库不为空，说明服务端有人为操作或者故障需要建立error数据，并暂时移除acc数据库中的minion'''
            '''获取acc数据库中的accminion的minionid'''
            acc_lost_minion_list = AccHostList.objects.all()
            acc_lost_minionid = []
            for minion in acc_lost_minion_list:
                acc_lost_minionid.append(str(minion.minionid))
            '''暂时移除accminion'''
            AccHostList.objects.all().delete()
            '''创建异常数据'''
            for minionid in acc_lost_minionid:
                error = ErrorHostList.objects.create(minionid=minionid,
                                                     key_tag='error',
                                                     action='无',
                                                     remark='acc组minion连接可能有问题,请核实！')
                error.save()
    else:
        '''如果服务器返回的minionid不是空的，先查看获取到的minionid在不在数据库，不在的就创建数据，在的就更新数据'''
        '''数据库的acc minionid为空就直接创建数据'''
        if all_acc_minionid == []:
            for acc_id in acc_stdout:
                acc_minion = AccHostList.objects.create(minionid=str(acc_id),
                                          hostname=all_host[str(acc_id)],
                                          nip=all_fqdn_ip4[str(acc_id)],
                                          osfinger=all_osfinger[str(acc_id)],
                                          mem_total=all_mem_total[str(acc_id)],
                                          cpu_model=all_cpu_model[str(acc_id)],
                                          num_cpus=all_num_cpus[str(acc_id)],
                                          cpuarch=all_cpuarch[str(acc_id)],
                                          kernelrelease=all_kernelrelease[str(acc_id)],
                                          saltversion=all_saltversion[str(acc_id)],
                                          key_tag='acc',
                                          action='无')
                acc_minion.save()
            '''此时加一层判断，因为数据库的acc minion为空的话可能在unacc的minion里面，此时就应该删除unacc的数据并且建立error数据做提示'''
            if all_unacc_minion == []:
                pass
            else:
                for acc_id in acc_stdout:
                    if str(acc_id) in all_unacc_minion:
                        UnAccHostList.objects.filter(minionid=str(acc_id)).delete()
                        '''建立异常数据的同时也要判断这个异常数据是否已经存在，存在的pass，不存在创建'''
                        wether_error = ErrorHostList.objects.filter(minionid=acc_id)
                        if wether_error == []:
                            pass
                        else:
                            error = ErrorHostList.objects.create(minionid=acc_id,
                                                                 key_tag='error',
                                                                 action='无',
                                                                 remark='acc组minion异常出现在unacc，已在unacc移除,请核实！')
                            error.save()
        else:
            '''数据库的acc minionid不为空,先查看获取到的minionid在不在数据库，不在的就创建数据'''
            for acc_id in acc_stdout:
                if acc_id not in all_acc_minionid:
                    acc_minion = AccHostList.objects.create(minionid=str(acc_id),
                                                            hostname=all_host[str(acc_id)],
                                                            nip=all_fqdn_ip4[str(acc_id)],
                                                            osfinger=all_osfinger[str(acc_id)],
                                                            mem_total=all_mem_total[str(acc_id)],
                                                            cpu_model=all_cpu_model[str(acc_id)],
                                                            num_cpus=all_num_cpus[str(acc_id)],
                                                            cpuarch=all_cpuarch[str(acc_id)],
                                                            kernelrelease=all_kernelrelease[str(acc_id)],
                                                            saltversion=all_saltversion[str(acc_id)],
                                                            key_tag='acc',
                                                            action='无')
                    acc_minion.save()
                    '''同样，如果服务端返回的数据不在acc，就有可能在unacc，再次判断并建立异常数据'''
                    wether_error = ErrorHostList.objects.filter(minionid=acc_id)
                    if wether_error == []:
                        pass
                    else:
                        error = ErrorHostList.objects.create(minionid=acc_id,
                                                             key_tag='error',
                                                             action='无',
                                                             remark='acc组minion异常出现在unacc，已在unacc移除,请核实！')
                        error.save()
                elif acc_id in all_acc_minionid:
                    '''数据库的acc minionid不为空,先查看获取到的minionid在不在数据库，在的就更新数据'''
                    acc_minion = AccHostList.objects.filter(minionid=str(acc_id)).update(nip=all_fqdn_ip4[str(acc_id)],
                                                                           hostname=all_host[str(acc_id)],
                                                                           osfinger=all_osfinger[str(acc_id)],
                                                                           mem_total=all_mem_total[str(acc_id)],
                                                                           cpu_model=all_cpu_model[str(acc_id)],
                                                                           num_cpus=all_num_cpus[str(acc_id)],
                                                                           cpuarch=all_cpuarch[str(acc_id)],
                                                                           kernelrelease=all_kernelrelease[str(acc_id)],
                                                                           saltversion=all_saltversion[str(acc_id)],
                                                                           key_tag='acc',
                                                                           action='无')
        #'''反向从数据库的minionid查看是否都在服务器返回的minionid列表中，在的pass'''
        for acc_id in all_acc_minionid:
            if str(acc_id) in acc_stdout:
                pass
            else:
                '''数据库的minionid不在服务器返回的minionid列表中，创建异常数据'''
                '''这时得看一下服务器返回的unacc的minion里面有没有当前minion，有的话就暂时移除当前accminion，在unacc创建数据，并且创建异常数据'''
                if unacc_stdout != ['']:
                    if str(acc_id) in unacc_stdout:
                        AccHostList.objects.get(minionid=str(acc_id)).delete()
                        '''先判断unacc是否已经有次minion，有的pass，没有的创建'''
                        if str(acc_id) in all_unacc_minionid:
                            pass
                        else:
                            unacc_from_acc = UnAccHostList.objects.create(minionid=str(acc_id))
                            unacc_from_acc.save()
                            wether_error = ErrorHostList.objects.filter(minionid=acc_id)
                            if wether_error == []:
                                pass
                            else:
                                error = ErrorHostList.objects.create(minionid=acc_id,
                                                                     key_tag='error',
                                                                     action='无',
                                                                     remark='acc组minion异常出现在服务器返回的unacc，已在数据库acc移除并且加入数据库的unacc,请核实！')
                                error.save()
                else:
                    '''先暂时移除异常acc数据再创建异常数据'''
                    AccHostList.objects.get(minionid=str(acc_id)).delete()
                    error = ErrorHostList.objects.create(minionid=str(acc_id),
                                                         key_tag='error',
                                                         action='无',
                                                         remark='acc组minion连接可能有问题,服务器并未返回此minionid，请核实！')
                    error.save()
    #'''接下来判断unacc'''
    #'''如果服务器返回的unacc在数据库中就pass，在acc中也不用处理，此前数据库反查，如果acc中的数据在数据库unacc和服务器返回的unacc中都不用处理'''
    if unacc_stdout == ['']:
        pass
    else:
        for unacc_id in unacc_stdout:
            if unacc_id in all_unacc_minion:
                pass
            elif unacc_id in all_acc_minion:
                pass
            else:
                '''但是数据库unacc和acc都没有的话就创建数据'''
                unacc_create = UnAccHostList.objects.create(minionid=str(unacc_id))
                unacc_create.save()



'''下面代码作废，以前写的，不知道写的啥。。。。'''
#        all_acc_id_in_db = []
#        for acc_id in acc_stdout:
#            all_acc = AccHostList.objects.all()
#            for acc_minion_in_db in all_acc:
#                all_acc_id_in_db.append(str(acc_minion_in_db.minionid))
#            if acc_id in all_acc_id_in_db:
#                '''更新数据'''
#                acc_minion = AccHostList
#                acc_minion.objects.filter(minionid=str(acc_id)).update(wip=all_fqdn_ip4[str(acc_id)],
#                                                                       hostname=all_host[str(acc_id)],
#                                                                       osfinger=all_osfinger[str(acc_id)],
#                                                                       mem_total=all_mem_total[str(acc_id)],
#                                                                       cpu_model=all_cpu_model[str(acc_id)],
#                                                                       num_cpus=all_num_cpus[str(acc_id)],
#                                                                       cpuarch=all_cpuarch[str(acc_id)],
#                                                                       kernelrelease=all_kernelrelease[str(acc_id)],
#                                                                       saltversion=all_saltversion[str(acc_id)],
#                                                                       key_tag='acc',
#                                                                       action='无')
#                acc_minion.save
#                acc_id_list.append(str(acc_id))
#            else:
#                '''创建数据'''
#                acc_minion = AccHostList
#                acc_minion.objects.create(hostname=all_host[str(acc_id)],
#                                          wip=all_fqdn_ip4[str(acc_id)],
#                                          osfinger=all_osfinger[str(acc_id)],
#                                          mem_total=all_mem_total[str(acc_id)],
#                                          cpu_model=all_cpu_model[str(acc_id)],
#                                          num_cpus=all_num_cpus[str(acc_id)],
#                                          cpuarch=all_cpuarch[str(acc_id)],
#                                          kernelrelease=all_kernelrelease[str(acc_id)],
#                                          saltversion=all_saltversion[str(acc_id)],
#                                          key_tag='acc',
#                                          action='无')
#                acc_minion.save
#                acc_id_list.append(str(acc_id))
#    '''获取unacc的minion_id'''
#    get_unacc_minion_id_cmd = "salt-key -l una|grep -v Una"
#    get_unacc_minion_id = subprocess.Popen(get_unacc_minion_id_cmd,stdout=subprocess.PIPE,shell=True)
#    unacc_stdout = get_unacc_minion_id.communicate()[0].strip().split('\n')
#    unacc_id_list = []
#    '''获取数据库中所有unacc的minion'''
#    if unacc_stdout == ['']:
#        all_unacc_minion = []
#    else:
#        all_unacc_minion = UnAccHostList.objects.filter(key_tag='unacc')
#        '''判断新增unacc是否已在数据库，有就获取数据，没有就create'''
#    if unacc_stdout == ['']:
#        pass
#    else:
#        all_unacc_id = []
#        for unacc_id in unacc_stdout:
#            all_unacc = UnAccHostList.objects.all()
#            for unacc_minion_in_db in all_unacc:
#                all_unacc_id.append(str(unacc_minion_in_db.minionid))
#            if unacc_id in all_unacc_id:
#                for unacc_id in unacc_stdout:
#                    unacc_minion = UnAccHostList
#                    unacc_minion.objects.filter(minionid=str(unacc_id)).update(hostname=str(unacc_id))
#                    unacc_minion.save
#                    unacc_id_list.append(str(unacc_id))
#            else:
#                for unacc_id in unacc_stdout:
#                    unacc_minion = UnAccHostList
#                    unacc_minion.objects.create(hostname=str(unacc_id),minionid=str(unacc_id),key_tag='unacc',action='<a class="btn btn-primary" onclick="accept()" href="/hostlist/accept_unacc/" >Accept</a>')
#                    unacc_minion.save
#                    unacc_id_list.append(str(unacc_id))
#    '''如果acc数据库更新之后的数据unacc还存在，删除unacc的数据'''
#    '''当前acchost'''
#    all_acc_in_db_id_now = []
#    all_acc_in_db_now = AccHostList.objects.all()
#    for acc_minion_in_db_now in all_acc_in_db_now:
#        all_acc_in_db_id_now.append(str(acc_minion_in_db_now.minionid))
#    '''当前unacchost'''
#    all_unacc_in_db_id_now = []
#    all_unacc_in_db_now = UnAccHostList.objects.all()
#    for unacc_minion_in_db in all_unacc_in_db_now:
#        all_unacc_in_db_id_now.append(str(unacc_minion_in_db.minionid))
#    '''acc和unacc当前数据库做对比acc自动更新'''
#    for acc_id_in_db in all_acc_in_db_id_now:
#        if acc_id_in_db in all_unacc_in_db_id_now:
#            print acc_id_in_db
#            del_unacc_minion_add = UnAccHostList
#            del_unacc_minion_add.objects.get(minionid=str(acc_id_in_db)).delete()
#            del_unacc_minion_add.save
#    '''2.反查数据库数据是否都在新增acc列表'''
#
#    for minion in all_acc_in_db_now:
#        if len(str(minion.wip)) > 15:
#            '''ip长度大于15，说明minion连接可能异常'''
#            '''删除minion在acc的数据'''
#            del_acc_minion = AccHostList
#            del_acc_minion.objects.filter(minionid=minion.minionid).delete()
#            del_acc_minion.save
#            error = ErrorHostList
#            '''创建异常数据'''
#            error.objects.get_or_create(minionid=minion.minionid)
#            error.save
#            error.objects.filter(minionid=minion.minionid).update(key_tag='error', action='无',
#                                                                  remark='acc组minion连接可能有问题,请核实！')
#            error.save
#            '''数据库中的acc的minion minionid和新增的一致说明数据没变化'''
#        elif minion.minionid in acc_id_list:
#            #print minion
#            #print acc_minion_list[0]
#            pass
#        elif minion.minionid not in acc_id_list:
#            if minion.minionid in unacc_id_list:
#                '''删除minion在acc的数据'''
#                del_acc_minion = AccHostList
#                del_acc_minion.objects.filter(minionid=minion.minionid, key_tag='acc').delete()
#                del_acc_minion.save
#                error = ErrorHostList
#                '''创建异常数据'''
#                error.objects.get_or_create(minionid=minion.minionid)
#                error.save
#                error.objects.filter(minionid=minion.minionid).update(key_tag='error', action='无',
#                                                                      remark='acc组minion异常迁移到unacc，且数据变更,请核实！')
#                error.save
#            else:
#                #print minion
#                #print acc_minion_list
#                error = ErrorHostList
#                error.objects.get_or_create(minionid=minion.minionid, key_tag='error', action='无',
#                                            remark='acc组minion异常丢失')
#                error.save
#                '''删除minion在acc的数据'''
#                print 'del start'
#
#                del_acc_minion = AccHostList
#                del_acc_minion.objects.filter(minionid=minion.minionid,key_tag='acc').delete()
#                del_acc_minion.save
#
#
#
#    '''判断unacc异常'''
#    for minion_un in all_unacc_in_db_now:
#        if minion_un.minionid in all_unacc_id:
#            pass
#        elif minion_un.minionid not in all_unacc_id:
#            if minion_un.minionid in acc_id_list:
#                error = ErrorHostList
#                '''创建异常数据'''
#                error.objects.get_or_create(minionid=minion_un.minionid,key_tag = 'error', action = '无', remark = 'unacc组minion异常迁移到acc')
#                error.save
#                '''删除minion在unacc的数据'''
#                del_unacc_minion = UnAccHostList
#                del_unacc_minion.objects.filter(minionid=minion_un.minionid,key_tag='unacc').delete()
#                del_unacc_minion.save
#            else :
#                error = ErrorHostList
#                error.objects.get_or_create(minionid=minion.minionid, key_tag='error', action='无',
#                                            remark='unacc组minion异常丢失')
#                error.save
#
#
#if __name__ == "__main__":
#    GetMinionInfo()

