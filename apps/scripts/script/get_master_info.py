#_*_coding:utf-8_*_
from __future__ import unicode_literals
import os,sys,subprocess,time
os.path.join(os.path.dirname(__file__),'../../..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AssetManage.settings')
import django
django.setup()
from dashboard.models import MasterLoadAvg,MasterProcessStatus,MinionOnlineNumber


def get_cpuload():
    cpuload_info = {}
    with open('/proc/loadavg', 'r') as loadavg:
        cpuload = loadavg.readline()
    cpuloads = []
    for load in cpuload.split(' '):
        cpuloads.append(str(load))
    cpuload_info[str('one')] = str(cpuloads[0])
    cpuload_info[str('five')] = str(cpuloads[1])
    cpuload_info[str('fifteen')] = str(cpuloads[2])
    cpuload_info[str('processes')] = str(cpuloads[3])
    cpuload_info[str('nowprocesspid')] = str(cpuloads[4])
    cpuload_info[str('updatetime')] = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
    return cpuload_info

def MasterInfo():
    loadavgdict = get_cpuload()
    MasterLoadAvg.objects.create(updatetime=str(loadavgdict['updatetime']),
                                 one=str(loadavgdict['one']),
                                 five=str(loadavgdict['five']),
                                 fifteen=str(loadavgdict['fifteen']),
                                 processes=str(loadavgdict['processes']),
                                 nowprocesspid=str(loadavgdict['nowprocesspid']),
                                 )

def get_master_process():
    master_ps_command = 'ps -ef|grep /usr/bin/salt-master|wc -l'
    master_ps = subprocess.Popen(master_ps_command, stdout=subprocess.PIPE, shell=True)
    master_ps_stdout = master_ps.communicate()[0].strip('\n')
    status = {}
    if int(master_ps_stdout) < 1:
        master_status = str('stop')
        status[str('updatetime')] = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
        status[str('status')] = str(master_status)
    else:
        master_status = str('normal')
        status[str('updatetime')] = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        status[str('status')] = str(master_status)
    return status

def Masterprocessstatus():
    master_status_dict = get_master_process()
    MasterProcessStatus.objects.create(updatetime=str(master_status_dict['updatetime']),
                                        status=str(master_status_dict['status']),
                                        )

def get_minion_online():
    minion_online_command = 'salt \'*\' test.ping|grep -v \':\'|grep True|wc -l'
    minion_online = subprocess.Popen(minion_online_command, stdout=subprocess.PIPE, shell=True)
    minion_online_stdout =minion_online.communicate()[0].strip('\n')
    minion_offline_command = 'salt \'*\' test.ping|grep -v \':\'|grep -v True|wc -l'
    minion_offline = subprocess.Popen(minion_offline_command, stdout=subprocess.PIPE, shell=True)
    minion_offline_stdout =minion_offline.communicate()[0].strip('\n')
    online = int(minion_online_stdout)
    offline = int(minion_offline_stdout)
    all = online + offline
    updatetime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    all_online_offline = [updatetime,all,online,offline]
    return all_online_offline

def Miniononline():
    all_online_offline_minions = get_minion_online()
    MinionOnlineNumber.objects.create(updatetime=str(all_online_offline_minions[0]),
                                      all=int(all_online_offline_minions[1]),
                                      online=int(all_online_offline_minions[2]),
                                      offline=int(all_online_offline_minions[3]),
                                      )