#_*_coding:utf-8_*_
from __future__ import unicode_literals

import os,sys,subprocess,time
os.path.join(os.path.dirname(__file__),'../../..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AssetManage.settings')
import django
django.setup()

from dashboard.models import MinionLoadAvg
'''dashboard需要持续获取的minion数据'''

'''获取minion端的信息(适用于centos)'''


All_minion_cmd = subprocess.Popen("salt-key -l acc|grep -v Acc",stdout=subprocess.PIPE,shell=True)
All_minion = All_minion_cmd.communicate()[0].strip().split('\n')
minions = []
for minion in All_minion:
    minions.append(minion)

def get_cpuload():
    getall_cpuload = {}
    for minion in minions:
        cpuload_info = {}
        cpuinfo = []
        all_cpuload_cmd = "salt " + str(minion) + " cmd.run \'cat /proc/loadavg\'|tail -1"
        all_cpuload = subprocess.Popen(all_cpuload_cmd, stdout=subprocess.PIPE, shell=True)
        all_cpuload_stdout = all_cpuload.communicate()[0].strip()
        for info in all_cpuload_stdout.split(' '):
            cpuinfo.append(str(info))
        cpuload_info[str('one')] = str(cpuinfo[0])
        cpuload_info[str('five')] = str(cpuinfo[1])
        cpuload_info[str('fifteen')] = str(cpuinfo[2])
        cpuload_info[str('processes')] = str(cpuinfo[3])
        cpuload_info[str('nowprocesspid')] = str(cpuinfo[4])
        cpuload_info[str('updatetime')] = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
        getall_cpuload[str(minion)] = cpuload_info
    return getall_cpuload

def get_mem():
    getall_mem = {}
    for minion in minions:
        all_mem_cmd = "salt " + str(minion) + " cmd.run \'free -m|head -4|tail -3\'|tail -3"
        all_mem = subprocess.Popen(all_mem_cmd, stdout=subprocess.PIPE, shell=True)
        all_mem_stdout = all_mem.communicate()[0].strip().split(':\n    ')
        mem = {}
        mem_info_list = []
        for mem_line in all_mem_stdout:
            mem_info_list.append(str(mem_line))
        buffers_cached_line = mem_info_list[0]
        buffer_cache_list = []
        for buffer_cache in buffers_cached_line.strip('\n').split('        '):
            buffer_cache_list.append(buffer_cache)
        for buffer in buffer_cache_list[-2:-1]:
            mem['buffers: '] = str(buffer)
        for cache in buffer_cache_list[-1:]:
            mem['cached: '] = str(cache)
        trust_mem_used_free_info_line = mem_info_list[1]
        mem_used_free_list = []
        for mem_used_free in trust_mem_used_free_info_line.strip('\n').split('        '):
            mem_used_free_list.append(str(mem_used_free))
        for mem_used in mem_used_free_list[-2:-1]:
            mem['mem_used: '] = str(mem_used)
        for mem_free in mem_used_free_list[-1:]:
          mem['mem_free: '] = str(mem_free)
        swap_used_free_line = mem_info_list[2]
        swap_used_free_list = []
        for swap_used_free in swap_used_free_line.strip('\n').split('        '):
            swap_used_free_list.append(str(swap_used_free))
        for swap_used in swap_used_free_list[-2:-1]:
            mem['swap_used: '] = str(swap_used)
        for swap_free in mem_used_free_list[-1:]:
            mem['swap_free: '] = str(swap_free)
        getall_mem[str(minion)] = mem
    print getall_mem
    return getall_mem



def DashboardInfos():
    get_cpuloads = get_cpuload()
    for minion,loadavgdict in get_cpuloads.items():
        MinionLoadAvg.objects.create(updatetime=str(loadavgdict['updatetime']),
                                     one=str(loadavgdict['one']),
                                     five=str(loadavgdict['five']),
                                     fifteen=str(loadavgdict['fifteen']),
                                     processes=str(loadavgdict['processes']),
                                     nowprocesspid=str(loadavgdict['nowprocesspid']),
                                     minionid=str(minion)
                                     )

dashboardinfo = DashboardInfos()

#get_cpuload()
#get_mem()