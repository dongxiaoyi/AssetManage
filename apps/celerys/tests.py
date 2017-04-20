#_*_coding:utf-8_*_
import subprocess,time
def get_master_process():
    master_ps_command = 'ps -ef|grep /usr/bin/salt-master|wc -l'
    master_ps = subprocess.Popen(master_ps_command, stdout=subprocess.PIPE, shell=True)
    master_ps_stdout = master_ps.communicate()[0].strip('\n')
    print master_ps_stdout
    status = {}
    if int(master_ps_stdout) < 1:
        master_status = str('stop')
        status[str('updatetime')] = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
        status[str('status')] = str(master_status)
    else:
        master_status = str('normal')
        status[str('updatetime')] = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        status[str('status')] = str(master_status)
    print status
    return status

get_master_process()