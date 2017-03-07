#_*_coding:utf-8_*_
#from AssetManage.celery import app
import subprocess
import sys,os


#os.environ['DJANGO_SETTINGS_MODULE'] = 'AssetManage.settings'
#@app.task
def GetAccMinionId():
    '''
    定时任务，推送通过验证的minion_id的资源信息到数据库
    :return:
    '''
    '''获取通过验证的minion_id'''
    acc_minion_id = []
    get_acc_minion_id_cmd = "salt-key -l acc|grep -v Acc"
    get_acc_minion_id = subprocess.Popen(get_acc_minion_id_cmd,stdout=subprocess.PIPE,shell=True)
    stdout = get_acc_minion_id.communicate()[0].strip().split('\n')
    for acc_id in stdout:
        acc_minion = AccHostList()
        acc_minion.objects.get_or_create(minionid=acc_id)
        acc_minion.save()

GetAccMinionId()
#GetAccMinionOsfinger()
def GetAccMinionOsfinger():
    '''获取通过验证的minion的系统版本'''
    acc_minion_osfinger = {}
    get_acc_minion_finger_cmd = "salt '*' grains.get osfinger|sed 'N;s/\\n//g'|sed 's/ //g'"
    get_acc_minion_finger = subprocess.Popen(get_acc_minion_finger_cmd,stdout=subprocess.PIPE,shell=True)
    stdout = get_acc_minion_finger.communicate()[0].strip().split('\n')
    for acc_osfinger in stdout:
        acc_minion_osfinger[acc_osfinger.split(':')[0]] = acc_osfinger.split(':')[1]
    return acc_minion_osfinger

def GetAccMinionfqdn_ip4():
    '''获取通过验证的minion的ip'''
    acc_minion_fqdn_ip4 = {}
    get_acc_minion_fqdn_ip4_cmd = "salt '*' cmd.run 'salt-call grains.get fqdn_ip4'|grep -v local|sed 'N;s/\\n//g'|sed 's/ //g'|sed 's/-//g'"
    get_acc_minion_fqdn_ip4 = subprocess.Popen(get_acc_minion_fqdn_ip4_cmd,stdout=subprocess.PIPE,shell=True)
    stdout = get_acc_minion_fqdn_ip4.communicate()[0].strip().split('\n')
    for acc_fqdn_ip4 in stdout:
        acc_minion_fqdn_ip4[acc_fqdn_ip4.split(':')[0]] = acc_fqdn_ip4.split(':')[1]
    print acc_minion_fqdn_ip4
    return acc_minion_fqdn_ip4

def GetAccMinionmachine_id():
    '''获取通过验证的minion的ip'''
    acc_minion_machine_id = {}
    get_acc_minion_machine_id_cmd = "salt '*' cmd.run 'salt-call grains.get machine_id'|grep -v local|sed 'N;s/\\n//g'|sed 's/ //g'|sed 's/-//g'"
    get_acc_minion_machine_id = subprocess.Popen(get_acc_minion_machine_id_cmd,stdout=subprocess.PIPE,shell=True)
    stdout = get_acc_minion_machine_id.communicate()[0].strip().split('\n')
    for acc_machine_id in stdout:
        acc_minion_machine_id[acc_machine_id.split(':')[0]] = acc_machine_id.split(':')[1]
    print acc_minion_machine_id
    return acc_minion_machine_id

def AccHostInfo():
    host = AccHostList()
    ip = GetAccMinionfqdn_ip4()
    mac_id = GetAccMinionmachine_id()
    minion_id = GetAccMinionId()
    os = GetAccMinionOsfinger()
    host.objects.get_or_create()