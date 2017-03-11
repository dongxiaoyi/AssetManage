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


def GetAccMinionOsfinger():
    '''获取通过验证的minion的系统版本'''
    acc_minion_osfinger = {}
    get_acc_minion_finger_cmd = "salt '*' grains.get osfinger|sed 'N;s/\\n//g'|sed 's/ //g'"
    get_acc_minion_finger = subprocess.Popen(get_acc_minion_finger_cmd,stdout=subprocess.PIPE,shell=True)
    stdout = get_acc_minion_finger.communicate()[0].strip().split('\n')
    for acc_osfinger in stdout:
        acc_minion_osfinger[str(acc_osfinger.split(':')[0])] = str(acc_osfinger.split(':')[1])
    return acc_minion_osfinger

def GetAccMinionfqdn_ip4():
    '''获取通过验证的minion的ip'''
    acc_minion_fqdn_ip4 = {}
    get_acc_minion_fqdn_ip4_cmd = "salt '*' cmd.run 'salt-call grains.get fqdn_ip4|head -2'|grep -v local|sed 'N;s/\\n//g'|sed 's/ //g'|sed 's/:-/:/g'"
    get_acc_minion_fqdn_ip4 = subprocess.Popen(get_acc_minion_fqdn_ip4_cmd,stdout=subprocess.PIPE,shell=True)
    stdout = get_acc_minion_fqdn_ip4.communicate()[0].strip().split('\n')
    for acc_fqdn_ip4 in stdout:
        acc_minion_fqdn_ip4[str(acc_fqdn_ip4.split(':')[0])] = str(acc_fqdn_ip4.split(':')[1])
    #print acc_minion_fqdn_ip4
    return acc_minion_fqdn_ip4
#GetAccMinionfqdn_ip4()
def GetAccMinionmachine_id():
    '''获取通过验证的minion的ip'''
    acc_minion_machine_id = {}
    get_acc_minion_machine_id_cmd = "salt '*' cmd.run 'salt-call grains.get machine_id'|grep -v local|sed 'N;s/\\n//g'|sed 's/ //g'|sed 's/:-/:/g'"
    get_acc_minion_machine_id = subprocess.Popen(get_acc_minion_machine_id_cmd,stdout=subprocess.PIPE,shell=True)
    stdout = get_acc_minion_machine_id.communicate()[0].strip().split('\n')
    for acc_machine_id in stdout:
        acc_minion_machine_id[str(acc_machine_id.split(':')[0])] = str(acc_machine_id.split(':')[1])
    return acc_minion_machine_id


def GetMinionInfo():
    '''
    定时任务，推送通过验证的minion_id的资源信息到数据库
    :return:

    '''
    '''所有的资源信息'''
    all_osfinger = GetAccMinionOsfinger()
    all_fqdn_ip4 = GetAccMinionfqdn_ip4()
    all_mac_id = GetAccMinionmachine_id()
    '''获取acc的minion_id'''
    get_acc_minion_id_cmd = "salt-key -l acc|grep -v Acc"
    get_acc_minion_id = subprocess.Popen(get_acc_minion_id_cmd,stdout=subprocess.PIPE,shell=True)
    acc_stdout = get_acc_minion_id.communicate()[0].strip().split('\n')
    acc_id_list = []
    '''获取数据库中所有acc的minion'''
    if acc_stdout == ['']:
        all_acc_minion = []
    else:
        all_acc_minion = AccHostList.objects.filter(key_tag='acc')

    '''如果这个minionid本来就有，就更新数据，没有就创建数据,如果这个minionid在unacc中，自动创建acc，并且删除unacc数据'''
    if acc_stdout == ['']:
        pass
    else:
        all_acc_id_in_db = []
        for acc_id in acc_stdout:
            all_acc = AccHostList.objects.all()
            for acc_minion_in_db in all_acc:
                all_acc_id_in_db.append(str(acc_minion_in_db.minionid))
            if acc_id in all_acc_id_in_db:
                '''更新数据'''
                acc_minion = AccHostList
                acc_minion.objects.filter(minionid=str(acc_id)).update(hostname=str(acc_id),ip=all_fqdn_ip4[str(acc_id)],mac_id=all_mac_id[str(acc_id)],osfinger=all_osfinger[str(acc_id)],
                              key_tag='acc',action='无')
                acc_minion.save
                acc_id_list.append(str(acc_id))
            else:
                '''创建数据'''
                acc_minion = AccHostList
                acc_minion.objects.create(hostname=str(acc_id), minionid=str(acc_id),
                                                                        ip=all_fqdn_ip4[str(acc_id)],
                                                                        mac_id=all_mac_id[str(acc_id)],
                                                                        osfinger=all_osfinger[str(acc_id)],
                                                                        key_tag='acc', action='无')
                acc_minion.save
                acc_id_list.append(str(acc_id))
    '''获取unacc的minion_id'''
    get_unacc_minion_id_cmd = "salt-key -l una|grep -v Una"
    get_unacc_minion_id = subprocess.Popen(get_unacc_minion_id_cmd,stdout=subprocess.PIPE,shell=True)
    unacc_stdout = get_unacc_minion_id.communicate()[0].strip().split('\n')
    unacc_id_list = []
    '''获取数据库中所有unacc的minion'''
    if unacc_stdout == ['']:
        all_unacc_minion = []
    else:
        all_unacc_minion = UnAccHostList.objects.filter(key_tag='unacc')
        '''判断新增unacc是否已在数据库，有就获取数据，没有就create'''
    if unacc_stdout == ['']:
        pass
    else:
        all_unacc_id = []
        for unacc_id in unacc_stdout:
            all_unacc = UnAccHostList.objects.all()
            for unacc_minion_in_db in all_unacc:
                all_unacc_id.append(str(unacc_minion_in_db.minionid))
            if unacc_id in all_unacc_id:
                for unacc_id in unacc_stdout:
                    unacc_minion = UnAccHostList
                    unacc_minion.objects.filter(minionid=str(unacc_id)).update(hostname=str(unacc_id))
                    unacc_minion.save
                    unacc_id_list.append(str(unacc_id))
            else:
                for unacc_id in unacc_stdout:
                    unacc_minion = UnAccHostList
                    unacc_minion.objects.create(hostname=str(unacc_id),minionid=str(unacc_id),key_tag='unacc',action='<a class="btn btn-primary" onclick="accept()" href="/hostlist/accept_unacc/" >Accept</a>')
                    unacc_minion.save
                    unacc_id_list.append(str(unacc_id))
    '''如果acc数据库更新之后的数据unacc还存在，删除unacc的数据'''
    '''当前acchost'''
    all_acc_in_db_id_now = []
    all_acc_in_db_now = AccHostList.objects.all()
    for acc_minion_in_db_now in all_acc_in_db_now:
        all_acc_in_db_id_now.append(str(acc_minion_in_db_now.minionid))
    '''当前unacchost'''
    all_unacc_in_db_id_now = []
    all_unacc_in_db_now = UnAccHostList.objects.all()
    for unacc_minion_in_db in all_unacc_in_db_now:
        all_unacc_in_db_id_now.append(str(unacc_minion_in_db.minionid))
    '''acc和unacc当前数据库做对比acc自动更新'''
    for acc_id_in_db in all_acc_in_db_id_now:
        if acc_id_in_db in all_unacc_in_db_id_now:
            print acc_id_in_db
            del_unacc_minion_add = UnAccHostList
            del_unacc_minion_add.objects.get(minionid=str(acc_id_in_db)).delete()
            del_unacc_minion_add.save
    '''2.反查数据库数据是否都在新增acc列表'''
    '''有些问题，需要修改'''
    '''celery和单独提取的orm可能有冲突，做脚本与计划任务的分离工作！！！'''
    for minion in all_acc_minion:
        if len(str(minion.ip)) > 15:
            '''ip长度大于15，说明minion连接可能异常'''
            '''删除minion在acc的数据'''
            del_acc_minion = AccHostList
            del_acc_minion.objects.filter(minionid=minion.minionid).delete()
            del_acc_minion.save
            error = ErrorHostList
            '''创建异常数据'''
            error.objects.get_or_create(minionid=minion.minionid)
            error.save
            error.objects.filter(minionid=minion.minionid).update(key_tag='error', action='无',
                                                                  remark='acc组minion连接可能有问题,请核实！')
            error.save
            '''数据库中的acc的minion minionid和新增的一致说明数据没变化'''
        elif minion.minionid in acc_id_list:
            #print minion
            #print acc_minion_list[0]
            pass
        elif minion.minionid not in acc_id_list:
            if unacc_minion_list != []:
                if minion.minionid in unacc_id_list:
                    '''删除minion在acc的数据'''
                    del_acc_minion = AccHostList
                    del_acc_minion.objects.filter(minionid=minion.minionid, key_tag='acc').delete()
                    del_acc_minion.save
                    error = ErrorHostList
                    '''创建异常数据'''
                    error.objects.get_or_create(minionid=minion.minionid)
                    error.save
                    error.objects.filter(minionid=minion.minionid).update(key_tag='error', action='无',
                                                                          remark='acc组minion异常迁移到unacc，且数据变更,请核实！')
                    error.save
            else:
                #print minion
                #print acc_minion_list
                error = ErrorHostList
                error.objects.get_or_create(minionid=minion.minionid, key_tag='error', action='无',
                                            remark='acc组minion异常丢失')
                error.save
                '''删除minion在acc的数据'''
                print 'del start'

                del_acc_minion = AccHostList
                del_acc_minion.objects.filter(minionid=minion.minionid,key_tag='acc').delete()
                del_acc_minion.save



    '''判断unacc异常'''
    #print unacc_minion_list
    for minion_un in all_unacc_minion:
        if minion_un.minionid in all_unacc_id:
            pass
        elif minion_un.minionid not in all_unacc_id:
            if all_acc_id != []:
                if minion_un.minionid in all_unacc_id:
                    error = ErrorHostList
                    '''创建异常数据'''
                    error.objects.get_or_create(minionid=minion_un.minionid,key_tag = 'error', action = '无', remark = 'unacc组minion异常迁移到acc')
                    error.save
                    '''删除minion在unacc的数据'''
                    del_unacc_minion = UnAccHostList
                    del_unacc_minion.objects.filter(minionid=minion_un.minionid,key_tag='unacc').delete()
                    del_unacc_minion.save
        else :
            error = ErrorHostList
            error.objects.get_or_create(minionid=minion.minionid, key_tag='error', action='无',
                                        remark='unacc组minion异常丢失')
            error.save


if __name__ == "__main__":
    GetMinionInfo()
#GetAccMinionOsfinger()

