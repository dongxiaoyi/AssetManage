#_*_coding:utf-8_*_
#from AssetManage.celery import app
import subprocess


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
        acc_minion_id.append(acc_id)
def GetAccMinionOsfinger():
    '''获取通过验证的minion的系统版本'''
    acc_minion_osfinger = {}
    get_acc_minion_finger_cmd = "salt '*' grains.get osfinger|sed 'N;s/\\n//g'|sed 's/ //g'"
    get_acc_minion_finger = subprocess.Popen(get_acc_minion_finger_cmd,stdout=subprocess.PIPE,shell=True)
    stdout = get_acc_minion_finger.communicate()[0].strip().split('\n')
    for acc_osfinger in stdout:
        acc_minion_osfinger[acc_osfinger.split(':')[0]] = acc_osfinger.split(':')[1]
    return acc_minion_osfinger

GetAccMinionOsfinger()



