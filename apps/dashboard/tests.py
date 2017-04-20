from django.test import TestCase
import subprocess,time
# Create your tests here.
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
    print all_online_offline
    print all_online_offline[0]
    print all_online_offline[1]
    return all_online_offline

def get_all_num_cpus():
    all_num_cpus = {}
    get_num_cpus_cmd = "salt " + '*' + " grains.get num_cpus|sed 'N;s/\\n//g'"
    get_num_cpus = subprocess.Popen(get_num_cpus_cmd,stdout=subprocess.PIPE,shell=True)
    num_cpus = get_num_cpus.communicate()[0].strip().split(':    ')
    print num_cpus
    for i in num_cpus:
        all_num_cpus[str('aaa')] = str(i)
    print all_num_cpus
    return all_num_cpus
get_all_num_cpus()